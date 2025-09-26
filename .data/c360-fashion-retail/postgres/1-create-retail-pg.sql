CREATE DATABASE retail_fashion;

\c retail_fashion;

-- Dumped from database version 17.6 (Debian 17.6-1.pgdg13+1)
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: assess_data_compatibility(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.assess_data_compatibility() RETURNS TABLE(assessment_type text, table_name text, column_name text, total_rows bigint, non_null_rows bigint, convertible_rows bigint, conversion_success_rate numeric, sample_unconvertible text[], max_length integer, recommended_action text)
    LANGUAGE plpgsql
    AS $_$
DECLARE
    table_rec RECORD;
    sql_text TEXT;
    result_record RECORD;
BEGIN
    -- Assess customer_id columns
    FOR table_rec IN 
        SELECT t.table_name, t.column_name, t.data_type
        FROM information_schema.columns t
        WHERE t.table_schema = 'public' 
          AND t.column_name LIKE '%customer_id%'
          AND t.table_name != 'customers' -- Skip the reference table
    LOOP
        sql_text := format('
            WITH assessment AS (
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT(%I) as non_null_rows,
                    COUNT(CASE WHEN %I ~ ''^\\d+$'' THEN 1 END) as convertible_rows,
                    MAX(LENGTH(%I::text)) as max_length
                FROM %I
            ),
            samples AS (
                SELECT ARRAY(
                    SELECT DISTINCT %I::text 
                    FROM %I 
                    WHERE %I IS NOT NULL 
                      AND NOT (%I ~ ''^\\d+$'')
                    LIMIT 5
                ) as unconvertible_samples
            )
            SELECT 
                a.total_rows,
                a.non_null_rows, 
                a.convertible_rows,
                CASE WHEN a.non_null_rows > 0 
                     THEN ROUND(a.convertible_rows * 100.0 / a.non_null_rows, 2)
                     ELSE 100.0 END as success_rate,
                s.unconvertible_samples,
                a.max_length
            FROM assessment a CROSS JOIN samples s',
            table_rec.column_name, table_rec.column_name, table_rec.column_name,
            table_rec.table_name, table_rec.column_name, table_rec.table_name,
            table_rec.column_name, table_rec.column_name
        );
        
        EXECUTE sql_text INTO result_record;
        
        RETURN QUERY SELECT 
            'customer_id_conversion'::text,
            table_rec.table_name,
            table_rec.column_name,
            result_record.total_rows,
            result_record.non_null_rows,
            result_record.convertible_rows,
            result_record.success_rate,
            result_record.unconvertible_samples,
            result_record.max_length,
            CASE 
                WHEN result_record.success_rate >= 95 THEN 'Safe to convert'
                WHEN result_record.success_rate >= 85 THEN 'Convert with cleanup'
                ELSE 'Manual intervention required'
            END;
    END LOOP;
    
    -- Assess product_id columns (converting integer to varchar)
    FOR table_rec IN 
        SELECT t.table_name, t.column_name, t.data_type
        FROM information_schema.columns t
        WHERE t.table_schema = 'public' 
          AND t.column_name LIKE '%product_id%'
          AND t.data_type = 'integer'
          AND t.table_name != 'products'
    LOOP
        sql_text := format('
            SELECT 
                COUNT(*) as total_rows,
                COUNT(%I) as non_null_rows,
                COUNT(%I) as convertible_rows, -- all integers can convert to varchar
                100.0 as success_rate,
                ARRAY[]::text[] as unconvertible_samples,
                MAX(LENGTH(%I::text)) as max_length
            FROM %I',
            table_rec.column_name, table_rec.column_name, table_rec.column_name, table_rec.table_name
        );
        
        EXECUTE sql_text INTO result_record;
        
        RETURN QUERY SELECT 
            'product_id_conversion'::text,
            table_rec.table_name,
            table_rec.column_name,
            result_record.total_rows,
            result_record.non_null_rows,
            result_record.convertible_rows,
            result_record.success_rate,
            result_record.unconvertible_samples,
            result_record.max_length,
            'Safe to convert (integer to varchar)'::text;
    END LOOP;
END;
$_$;


ALTER FUNCTION public.assess_data_compatibility() OWNER TO postgres;

--
-- Name: import_customers_batch(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.import_customers_batch(batch_size integer DEFAULT 500) RETURNS TABLE(batch_num integer, records_imported integer, status text)
    LANGUAGE plpgsql
    AS $$
DECLARE
    current_batch INTEGER := 1;
    records_processed INTEGER := 0;
    total_records INTEGER;
BEGIN
    -- Clear staging table
    TRUNCATE staging_customers;
    
    -- Import all data into staging first
    COPY staging_customers FROM '/docker-entrypoint-initdb.d/customers.csv' WITH CSV HEADER;
    
    GET DIAGNOSTICS total_records = ROW_COUNT;
    
    -- Process in batches
    WHILE records_processed < total_records LOOP
        -- Insert batch into final table with proper column mapping
        INSERT INTO customers (
            customer_id, email, phone, first_name, last_name, 
            date_of_birth, gender, acquisition_channel, registration_date,
            account_status, preferred_language, marketing_consent, 
            last_activity_date, created_at, updated_at
        )
        SELECT 
            s.customer_id, s.email, s.phone, s.first_name, s.last_name,
            s.date_of_birth, s.gender, s.acquisition_channel, s.registration_date,
            'active', 'en', true, -- Default values for missing columns
            COALESCE(s.last_login, s.registration_date), -- Map last_login to last_activity_date
            s.registration_date, -- created_at
            CURRENT_TIMESTAMP -- updated_at
        FROM staging_customers s
        WHERE s.customer_id > records_processed 
        AND s.customer_id <= records_processed + batch_size;
        
        GET DIAGNOSTICS records_imported = ROW_COUNT;
        records_processed := records_processed + batch_size;
        
        RETURN QUERY SELECT current_batch, records_imported, 'SUCCESS';
        current_batch := current_batch + 1;
        
        -- Small delay to prevent overwhelming system
        PERFORM pg_sleep(0.1);
    END LOOP;
    
    RETURN;
END;
$$;


ALTER FUNCTION public.import_customers_batch(batch_size integer) OWNER TO postgres;

--
-- Name: import_order_items_batch(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.import_order_items_batch(batch_size integer DEFAULT 500) RETURNS TABLE(batch_num integer, records_imported integer, status text)
    LANGUAGE plpgsql
    AS $$
DECLARE
    current_batch INTEGER := 1;
    records_processed INTEGER := 0;
    total_records INTEGER;
BEGIN
    TRUNCATE staging_order_items;
    
    COPY staging_order_items FROM '/docker-entrypoint-initdb.d/order_items.csv' WITH CSV HEADER;
    GET DIAGNOSTICS total_records = ROW_COUNT;
    
    WHILE records_processed < total_records LOOP
        INSERT INTO order_items (
            order_item_id, order_id, product_id, sku, quantity, 
            unit_price, total_price, discount_applied, final_price,
            size, color, personalization, gift_wrap
        )
        SELECT 
            s.order_item_id, s.order_id, s.variant_id, -- Map variant_id to product_id
            CONCAT('SKU-', s.variant_id), -- Generate SKU
            s.quantity, s.unit_price, s.total_price, s.discount_amount,
            s.total_price - COALESCE(s.discount_amount, 0), -- Calculate final_price
            'M', 'Default', -- Default size/color
            s.personalization_data::TEXT, false -- personalization, gift_wrap
        FROM staging_order_items s
        WHERE s.order_item_id > records_processed 
        AND s.order_item_id <= records_processed + batch_size;
        
        GET DIAGNOSTICS records_imported = ROW_COUNT;
        records_processed := records_processed + batch_size;
        
        RETURN QUERY SELECT current_batch, records_imported, 'SUCCESS';
        current_batch := current_batch + 1;
        
        PERFORM pg_sleep(0.1);
    END LOOP;
    
    RETURN;
END;
$$;


ALTER FUNCTION public.import_order_items_batch(batch_size integer) OWNER TO postgres;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.brands (
    brand_id integer NOT NULL,
    brand_name character varying(100) NOT NULL,
    parent_company character varying(100),
    brand_tier character varying(50),
    description text,
    website_url character varying(255),
    year_established integer,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT brands_brand_tier_check CHECK (((brand_tier)::text = ANY ((ARRAY['Luxury'::character varying, 'Premium'::character varying, 'Contemporary'::character varying, 'Fast Fashion'::character varying, 'Value'::character varying])::text[])))
);


ALTER TABLE public.brands OWNER TO postgres;

--
-- Name: brands_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.brands_brand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.brands_brand_id_seq OWNER TO postgres;

--
-- Name: brands_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.brands_brand_id_seq OWNED BY public.brands.brand_id;


--
-- Name: campaign_responses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaign_responses (
    response_id character varying(20) NOT NULL,
    campaign_id character varying(20),
    customer_id integer,
    sent_date timestamp without time zone,
    delivered_date timestamp without time zone,
    opened_date timestamp without time zone,
    clicked_date timestamp without time zone,
    converted_date timestamp without time zone,
    conversion_order_id character varying(20),
    conversion_amount numeric(10,2) DEFAULT 0,
    response_status character varying(20)
);


ALTER TABLE public.campaign_responses OWNER TO postgres;

--
-- Name: campaigns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaigns (
    campaign_id character varying(20) NOT NULL,
    campaign_name character varying(255) NOT NULL,
    campaign_type character varying(50),
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    target_audience character varying(100),
    budget_allocated numeric(12,2),
    budget_spent numeric(12,2),
    discount_offered integer DEFAULT 0,
    promo_code character varying(50),
    created_by character varying(50),
    status character varying(20)
);


ALTER TABLE public.campaigns OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    parent_category_id integer,
    description text,
    is_seasonal boolean DEFAULT false,
    typical_margin_percentage numeric(5,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_category_id_seq OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: column_type_assessment; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.column_type_assessment AS
 SELECT table_name,
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
        CASE
            WHEN ((column_name)::name ~~ '%customer_id%'::text) THEN 'customer_id_group'::text
            WHEN ((column_name)::name ~~ '%product_id%'::text) THEN 'product_id_group'::text
            WHEN ((column_name)::name ~~ '%order_id%'::text) THEN 'order_id_group'::text
            ELSE 'other'::text
        END AS column_group
   FROM information_schema.columns
  WHERE (((table_schema)::name = 'public'::name) AND (((column_name)::name ~~ '%customer_id%'::text) OR ((column_name)::name ~~ '%product_id%'::text) OR ((column_name)::name ~~ '%order_id%'::text)))
  ORDER BY
        CASE
            WHEN ((column_name)::name ~~ '%customer_id%'::text) THEN 'customer_id_group'::text
            WHEN ((column_name)::name ~~ '%product_id%'::text) THEN 'product_id_group'::text
            WHEN ((column_name)::name ~~ '%order_id%'::text) THEN 'order_id_group'::text
            ELSE 'other'::text
        END, table_name, column_name;


ALTER VIEW public.column_type_assessment OWNER TO postgres;

--
-- Name: current_foreign_keys; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.current_foreign_keys AS
 SELECT tc.table_name,
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
   FROM ((information_schema.table_constraints tc
     JOIN information_schema.key_column_usage kcu ON ((((tc.constraint_name)::name = (kcu.constraint_name)::name) AND ((tc.table_schema)::name = (kcu.table_schema)::name))))
     JOIN information_schema.constraint_column_usage ccu ON ((((ccu.constraint_name)::name = (tc.constraint_name)::name) AND ((ccu.table_schema)::name = (tc.table_schema)::name))))
  WHERE (((tc.constraint_type)::text = 'FOREIGN KEY'::text) AND ((tc.table_schema)::name = 'public'::name))
  ORDER BY tc.table_name, tc.constraint_name;


ALTER VIEW public.current_foreign_keys OWNER TO postgres;

--
-- Name: customer_addresses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer_addresses (
    address_id character varying(20) NOT NULL,
    customer_id integer,
    address_type character varying(20) NOT NULL,
    street_address text,
    city character varying(100),
    state_province character varying(50),
    postal_code character varying(20),
    country character varying(5) DEFAULT 'US'::character varying,
    is_primary boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.customer_addresses OWNER TO postgres;

--
-- Name: customer_service_interactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer_service_interactions (
    interaction_id character varying(20) NOT NULL,
    customer_id integer,
    interaction_date timestamp without time zone,
    channel character varying(20),
    interaction_type character varying(50),
    category character varying(50),
    priority character varying(10),
    subject_line character varying(255),
    conversation_text text,
    related_order_id character varying(20),
    resolution_type character varying(50),
    satisfaction_score integer,
    resolution_time_hours numeric(5,1),
    agent_id character varying(20),
    escalated boolean DEFAULT false,
    sentiment_score numeric(3,2),
    keywords_extracted text,
    follow_up_needed boolean DEFAULT false,
    interaction_cost numeric(8,2),
    CONSTRAINT customer_service_interactions_satisfaction_score_check CHECK (((satisfaction_score >= 1) AND (satisfaction_score <= 5)))
);


ALTER TABLE public.customer_service_interactions OWNER TO postgres;

--
-- Name: TABLE customer_service_interactions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.customer_service_interactions IS 'Customer service interaction tracking with sentiment analysis';


--
-- Name: customer_style_embeddings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer_style_embeddings (
    customer_embedding_id character varying(20) NOT NULL,
    customer_id character varying(20),
    style_vector text,
    text_source text,
    confidence_score numeric(4,4),
    last_updated timestamp without time zone,
    purchase_count_basis integer
);


ALTER TABLE public.customer_style_embeddings OWNER TO postgres;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    email character varying(255),
    phone character varying(20),
    first_name character varying(100),
    last_name character varying(100),
    date_of_birth date,
    gender character varying(20),
    acquisition_channel character varying(50),
    registration_date timestamp without time zone,
    account_status character varying(20) DEFAULT 'active'::character varying,
    preferred_language character varying(10) DEFAULT 'en'::character varying,
    marketing_consent boolean DEFAULT true,
    last_activity_date timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: data_compatibility_report; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.data_compatibility_report AS
 SELECT assessment_type,
    table_name,
    column_name,
    total_rows,
    non_null_rows,
    convertible_rows,
    conversion_success_rate,
    sample_unconvertible,
    max_length,
    recommended_action
   FROM public.assess_data_compatibility() assess_data_compatibility(assessment_type, table_name, column_name, total_rows, non_null_rows, convertible_rows, conversion_success_rate, sample_unconvertible, max_length, recommended_action);


ALTER VIEW public.data_compatibility_report OWNER TO postgres;

--
-- Name: email_engagement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.email_engagement (
    engagement_id character varying(20) NOT NULL,
    customer_id integer,
    campaign_id character varying(20),
    email_subject character varying(255),
    send_timestamp timestamp without time zone,
    delivery_status character varying(20),
    open_timestamp timestamp without time zone,
    total_opens integer DEFAULT 0,
    click_timestamp timestamp without time zone,
    total_clicks integer DEFAULT 0,
    links_clicked text,
    time_spent_reading integer DEFAULT 0,
    device_type character varying(20),
    email_client character varying(50),
    unsubscribe_timestamp timestamp without time zone,
    forward_count integer DEFAULT 0,
    ab_test_variant character varying(1)
);


ALTER TABLE public.email_engagement OWNER TO postgres;

--
-- Name: TABLE email_engagement; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.email_engagement IS 'Email campaign engagement metrics';


--
-- Name: fashion_research_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fashion_research_documents (
    document_id character varying(50) NOT NULL,
    document_type character varying(50),
    source character varying(100),
    title text,
    publication_date date,
    embedding_vector text,
    key_themes text,
    customer_segments text,
    trend_confidence numeric(3,2),
    geographic_focus character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.fashion_research_documents OWNER TO postgres;


--
-- Name: loyalty_activities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loyalty_activities (
    activity_id character varying(20) NOT NULL,
    customer_id integer,
    activity_type character varying(50),
    activity_date timestamp without time zone,
    points_earned integer DEFAULT 0,
    points_redeemed integer DEFAULT 0,
    description text,
    related_order_id character varying(20),
    expiry_date date
);


ALTER TABLE public.loyalty_activities OWNER TO postgres;

--
-- Name: loyalty_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loyalty_profiles (
    customer_id integer NOT NULL,
    tier_level character varying(20),
    points_balance integer DEFAULT 0,
    points_lifetime integer DEFAULT 0,
    tier_start_date date,
    next_tier_threshold integer,
    birthday_month integer,
    anniversary_date date,
    preferred_categories text,
    communication_preferences text,
    vip_status boolean DEFAULT false,
    last_tier_review date
);


ALTER TABLE public.loyalty_profiles OWNER TO postgres;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    order_item_id integer NOT NULL,
    order_id integer,
    product_id character varying(20),
    sku character varying(50),
    quantity integer,
    unit_price numeric(10,2),
    total_price numeric(10,2),
    discount_applied numeric(10,2),
    final_price numeric(10,2),
    size character varying(10),
    color character varying(50),
    personalization text,
    gift_wrap boolean DEFAULT false,
    CONSTRAINT chk_order_items_positive_values CHECK (((quantity > 0) AND (unit_price >= (0)::numeric) AND (total_price >= (0)::numeric) AND (final_price >= (0)::numeric) AND (discount_applied >= (0)::numeric))),
    CONSTRAINT chk_order_items_quantity_positive CHECK ((quantity > 0))
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    customer_id integer,
    order_date timestamp without time zone,
    order_status character varying(50),
    channel character varying(50),
    store_location character varying(100),
    subtotal_amount numeric(10,2),
    tax_amount numeric(10,2),
    shipping_amount numeric(10,2),
    discount_amount numeric(10,2),
    total_amount numeric(10,2),
    currency character varying(10) DEFAULT 'USD'::character varying,
    payment_method character varying(50),
    shipping_method character varying(50),
    promo_code character varying(50),
    is_first_order boolean DEFAULT false,
    device_type character varying(50),
    utm_source character varying(100),
    utm_campaign character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_orders_positive_amounts CHECK (((total_amount >= (0)::numeric) AND (subtotal_amount >= (0)::numeric) AND (tax_amount >= (0)::numeric) AND (shipping_amount >= (0)::numeric) AND (discount_amount >= (0)::numeric))),
    CONSTRAINT chk_orders_total_positive CHECK ((total_amount >= (0)::numeric))
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: product_embeddings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_embeddings (
    embedding_id character varying(20) NOT NULL,
    product_id character varying(20),
    text_source text,
    embedding_vector text,
    embedding_model character varying(50),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    vector_version integer DEFAULT 1
);


ALTER TABLE public.product_embeddings OWNER TO postgres;

--
-- Name: TABLE product_embeddings; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.product_embeddings IS 'Product embeddings for similarity matching';


--
-- Name: product_variants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_variants (
    variant_id integer NOT NULL,
    product_id character varying(20),
    sku character varying(100) NOT NULL,
    size character varying(20),
    color character varying(50),
    additional_price numeric(10,2) DEFAULT 0.00,
    weight_oz numeric(8,2),
    stock_quantity integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_product_variants_non_negative CHECK (((stock_quantity >= 0) AND (additional_price >= (0)::numeric) AND (weight_oz > (0)::numeric)))
);


ALTER TABLE public.product_variants OWNER TO postgres;

--
-- Name: product_variants_variant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_variants_variant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_variants_variant_id_seq OWNER TO postgres;

--
-- Name: product_variants_variant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_variants_variant_id_seq OWNED BY public.product_variants.variant_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id character varying(20) NOT NULL,
    product_name character varying(255) NOT NULL,
    brand character varying(100),
    category_l1 character varying(100),
    category_l2 character varying(100),
    category_l3 character varying(100),
    gender_target character varying(20),
    season character varying(50),
    material character varying(255),
    care_instructions character varying(50),
    sustainability_score integer DEFAULT 0,
    price_range character varying(50),
    launch_date date,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_products_sustainability_score CHECK (((sustainability_score >= 0) AND (sustainability_score <= 100)))
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: session_summary; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.session_summary (
    summary_date date,
    total_sessions integer,
    unique_visitors integer,
    bounce_sessions integer,
    avg_session_duration integer,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.session_summary OWNER TO postgres;

--
-- Name: realistic_conversion_metrics; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.realistic_conversion_metrics AS
 SELECT 'Conversion Analysis'::text AS metric,
    ( SELECT sum(session_summary.total_sessions) AS sum
           FROM public.session_summary) AS total_sessions,
    ( SELECT count(*) AS count
           FROM public.orders) AS total_orders,
    round(((( SELECT (count(*))::numeric AS count
           FROM public.orders) / ( SELECT (sum(session_summary.total_sessions))::numeric AS sum
           FROM public.session_summary)) * (100)::numeric), 2) AS conversion_rate_percent,
    'Realistic based on aggregated session data'::text AS note;


ALTER VIEW public.realistic_conversion_metrics OWNER TO postgres;

--
-- Name: return_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.return_items (
    return_item_id character varying(20) NOT NULL,
    return_id character varying(20),
    order_item_id integer,
    quantity_returned integer,
    item_condition text,
    refund_eligible boolean DEFAULT true,
    restockable boolean DEFAULT true,
    CONSTRAINT chk_return_items_positive_quantity CHECK ((quantity_returned > 0))
);


ALTER TABLE public.return_items OWNER TO postgres;

--
-- Name: returns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.returns (
    return_id character varying(20) NOT NULL,
    order_id integer,
    customer_id integer,
    return_date timestamp without time zone NOT NULL,
    return_reason character varying(255),
    return_method character varying(50),
    refund_amount numeric(10,2),
    refund_method character varying(50),
    return_status character varying(20),
    restocking_fee numeric(10,2) DEFAULT 0,
    condition_received character varying(100),
    processed_by character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_returns_positive_amounts CHECK (((refund_amount >= (0)::numeric) AND (restocking_fee >= (0)::numeric)))
);


ALTER TABLE public.returns OWNER TO postgres;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    customer_id integer,
    product_id integer,
    order_id integer,
    rating integer,
    review_title character varying(200),
    review_text text,
    verified_purchase boolean DEFAULT false,
    helpful_count integer DEFAULT 0,
    not_helpful_count integer DEFAULT 0,
    fit_rating character varying(20),
    quality_rating integer,
    style_rating integer,
    value_rating integer,
    sentiment_score numeric(3,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_reviews_rating CHECK (((rating >= 1) AND (rating <= 5))),
    CONSTRAINT reviews_fit_rating_check CHECK (((fit_rating)::text = ANY ((ARRAY['Runs Small'::character varying, 'True to Size'::character varying, 'Runs Large'::character varying])::text[]))),
    CONSTRAINT reviews_quality_rating_check CHECK (((quality_rating >= 1) AND (quality_rating <= 5))),
    CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
    CONSTRAINT reviews_style_rating_check CHECK (((style_rating >= 1) AND (style_rating <= 5))),
    CONSTRAINT reviews_value_rating_check CHECK (((value_rating >= 1) AND (value_rating <= 5)))
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_review_id_seq OWNER TO postgres;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: social_mentions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.social_mentions (
    mention_id character varying(20) NOT NULL,
    customer_id integer,
    platform character varying(50),
    post_url text,
    username character varying(100),
    post_date timestamp without time zone,
    post_type character varying(20),
    post_text text,
    hashtags text,
    mentions text,
    engagement_count integer DEFAULT 0,
    follower_count integer DEFAULT 0,
    sentiment_score numeric(3,2),
    brand_mentioned character varying(100),
    products_tagged character varying(20),
    influence_score integer DEFAULT 0,
    ugc_usage_rights boolean DEFAULT false,
    campaign_tagged character varying(20),
    CONSTRAINT chk_platform CHECK (((platform)::text = ANY ((ARRAY['Instagram'::character varying, 'TikTok'::character varying, 'Twitter'::character varying, 'Facebook'::character varying, 'Pinterest'::character varying])::text[]))),
    CONSTRAINT chk_post_type CHECK (((post_type)::text = ANY ((ARRAY['Post'::character varying, 'Story'::character varying, 'Reel'::character varying, 'Video'::character varying, 'Comment'::character varying])::text[])))
);


ALTER TABLE public.social_mentions OWNER TO postgres;

--
-- Name: TABLE social_mentions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.social_mentions IS 'Social media mentions and engagement data';


--
-- Name: staging_customer_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staging_customer_sessions (
    session_id character varying(50),
    customer_id integer,
    session_start timestamp without time zone,
    session_end timestamp without time zone,
    duration_minutes integer,
    page_views integer,
    pages_visited text[],
    products_viewed integer[],
    search_terms text[],
    device_type character varying(50),
    browser character varying(50),
    operating_system character varying(50),
    traffic_source character varying(100),
    utm_parameters jsonb,
    geo_location character varying(100),
    cart_value numeric(10,2),
    abandoned_cart boolean,
    conversion_event character varying(50),
    exit_page character varying(200)
);


ALTER TABLE public.staging_customer_sessions OWNER TO postgres;

--
-- Name: staging_order_items_simple; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staging_order_items_simple (
    order_item_id integer,
    order_id integer,
    variant_id integer,
    quantity integer,
    unit_price numeric(10,2),
    discount_amount numeric(10,2),
    total_price numeric(10,2),
    return_quantity integer,
    personalization_data jsonb
);


ALTER TABLE public.staging_order_items_simple OWNER TO postgres;

--
-- Name: style_similarity_matches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.style_similarity_matches (
    match_id character varying(20) NOT NULL,
    customer_id character varying(20),
    product_id character varying(20),
    similarity_score numeric(6,4),
    recommendation_type character varying(50),
    match_date timestamp without time zone,
    clicked boolean DEFAULT false,
    purchased boolean DEFAULT false,
    recommendation_context character varying(50)
);


ALTER TABLE public.style_similarity_matches OWNER TO postgres;

--
-- Name: TABLE style_similarity_matches; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.style_similarity_matches IS 'Customer to product recommendation matches based on style similarity';


--
-- Name: website_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.website_sessions (
    session_id character varying(20) NOT NULL,
    customer_id integer,
    anonymous_id character varying(20),
    session_start timestamp without time zone,
    session_end timestamp without time zone,
    duration_minutes numeric(8,1),
    page_views integer,
    pages_visited text,
    products_viewed text,
    search_terms text,
    device_type character varying(20),
    browser character varying(50),
    operating_system character varying(50),
    traffic_source character varying(50),
    utm_parameters text,
    geo_location character varying(100),
    cart_value numeric(10,2) DEFAULT 0,
    abandoned_cart boolean DEFAULT false,
    conversion_event character varying(50),
    exit_page character varying(255)
);


ALTER TABLE public.website_sessions OWNER TO postgres;

--
-- Name: TABLE website_sessions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.website_sessions IS 'Website session tracking and behavior analysis';


--
-- Name: brands brand_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brands ALTER COLUMN brand_id SET DEFAULT nextval('public.brands_brand_id_seq'::regclass);


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);




--
-- Name: product_variants variant_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants ALTER COLUMN variant_id SET DEFAULT nextval('public.product_variants_variant_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: brands brands_brand_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_brand_name_key UNIQUE (brand_name);


--
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (brand_id);


--
-- Name: campaign_responses campaign_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_responses
    ADD CONSTRAINT campaign_responses_pkey PRIMARY KEY (response_id);


--
-- Name: campaigns campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (campaign_id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: customer_addresses customer_addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer_addresses
    ADD CONSTRAINT customer_addresses_pkey PRIMARY KEY (address_id);


--
-- Name: customer_service_interactions customer_service_interactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer_service_interactions
    ADD CONSTRAINT customer_service_interactions_pkey PRIMARY KEY (interaction_id);


--
-- Name: customer_style_embeddings customer_style_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer_style_embeddings
    ADD CONSTRAINT customer_style_embeddings_pkey PRIMARY KEY (customer_embedding_id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: email_engagement email_engagement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_engagement
    ADD CONSTRAINT email_engagement_pkey PRIMARY KEY (engagement_id);


--
-- Name: fashion_research_documents fashion_research_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fashion_research_documents
    ADD CONSTRAINT fashion_research_documents_pkey PRIMARY KEY (document_id);




--
-- Name: loyalty_activities loyalty_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyalty_activities
    ADD CONSTRAINT loyalty_activities_pkey PRIMARY KEY (activity_id);


--
-- Name: loyalty_profiles loyalty_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyalty_profiles
    ADD CONSTRAINT loyalty_profiles_pkey PRIMARY KEY (customer_id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: product_embeddings product_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_embeddings
    ADD CONSTRAINT product_embeddings_pkey PRIMARY KEY (embedding_id);


--
-- Name: product_variants product_variants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants
    ADD CONSTRAINT product_variants_pkey PRIMARY KEY (variant_id);


--
-- Name: product_variants product_variants_sku_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants
    ADD CONSTRAINT product_variants_sku_key UNIQUE (sku);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: return_items return_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.return_items
    ADD CONSTRAINT return_items_pkey PRIMARY KEY (return_item_id);


--
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (return_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: social_mentions social_mentions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.social_mentions
    ADD CONSTRAINT social_mentions_pkey PRIMARY KEY (mention_id);


--
-- Name: style_similarity_matches style_similarity_matches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.style_similarity_matches
    ADD CONSTRAINT style_similarity_matches_pkey PRIMARY KEY (match_id);


--
-- Name: website_sessions website_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.website_sessions
    ADD CONSTRAINT website_sessions_pkey PRIMARY KEY (session_id);


--
-- Name: idx_brands_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_brands_name ON public.brands USING btree (brand_name);


--
-- Name: idx_brands_tier; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_brands_tier ON public.brands USING btree (brand_tier);


--
-- Name: idx_categories_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_categories_name ON public.categories USING btree (category_name);


--
-- Name: idx_categories_parent; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_categories_parent ON public.categories USING btree (parent_category_id);


--
-- Name: idx_product_variants_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_product_variants_product_id ON public.product_variants USING btree (product_id);


--
-- Name: idx_product_variants_sku; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_product_variants_sku ON public.product_variants USING btree (sku);


--
-- Name: idx_social_mentions_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_social_mentions_customer_id ON public.social_mentions USING btree (customer_id);


--
-- Name: idx_style_similarity_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_style_similarity_customer_id ON public.style_similarity_matches USING btree (customer_id);


--
-- Name: idx_style_similarity_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_style_similarity_product_id ON public.style_similarity_matches USING btree (product_id);


--
-- Name: idx_website_sessions_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_website_sessions_customer_id ON public.website_sessions USING btree (customer_id);


--
-- Name: campaign_responses campaign_responses_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_responses
    ADD CONSTRAINT campaign_responses_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES public.campaigns(campaign_id);


--
-- Name: categories categories_parent_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_category_id_fkey FOREIGN KEY (parent_category_id) REFERENCES public.categories(category_id);


--
-- Name: email_engagement email_engagement_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_engagement
    ADD CONSTRAINT email_engagement_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES public.campaigns(campaign_id);


--
-- Name: campaign_responses fk_campaign_responses_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_responses
    ADD CONSTRAINT fk_campaign_responses_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: customer_addresses fk_customer_addresses_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer_addresses
    ADD CONSTRAINT fk_customer_addresses_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: customer_service_interactions fk_customer_service_interactions_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer_service_interactions
    ADD CONSTRAINT fk_customer_service_interactions_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: email_engagement fk_email_engagement_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_engagement
    ADD CONSTRAINT fk_email_engagement_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: loyalty_activities fk_loyalty_activities_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyalty_activities
    ADD CONSTRAINT fk_loyalty_activities_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: loyalty_profiles fk_loyalty_profiles_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyalty_profiles
    ADD CONSTRAINT fk_loyalty_profiles_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: order_items fk_order_items_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_items_order_id FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: order_items fk_order_items_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_items_product_id FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: orders fk_orders_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_orders_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: product_variants fk_product_variants_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants
    ADD CONSTRAINT fk_product_variants_product_id FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: return_items fk_return_items_order_item_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.return_items
    ADD CONSTRAINT fk_return_items_order_item_id FOREIGN KEY (order_item_id) REFERENCES public.order_items(order_item_id);


--
-- Name: returns fk_returns_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT fk_returns_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: returns fk_returns_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT fk_returns_order_id FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: reviews fk_reviews_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: reviews fk_reviews_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_order_id FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: social_mentions fk_social_mentions_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.social_mentions
    ADD CONSTRAINT fk_social_mentions_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: website_sessions fk_website_sessions_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.website_sessions
    ADD CONSTRAINT fk_website_sessions_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: product_embeddings product_embeddings_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_embeddings
    ADD CONSTRAINT product_embeddings_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: return_items return_items_return_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.return_items
    ADD CONSTRAINT return_items_return_id_fkey FOREIGN KEY (return_id) REFERENCES public.returns(return_id);


--
-- Name: style_similarity_matches style_similarity_matches_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.style_similarity_matches
    ADD CONSTRAINT style_similarity_matches_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- PostgreSQL database dump complete
--

\unrestrict g7bUKWIv6sLlBRnt7yPasCEbL1SUmP43hOZ92X8UWUFG248Sh2it96UBTnHVpgk

