-- Populate style_similarity_matches table with realistic data
-- This table appears to track product recommendations and their outcomes

-- Generate sample style similarity matches
INSERT INTO style_similarity_matches (
    match_id,
    customer_id,
    product_id,
    similarity_score,
    recommendation_type,
    match_date,
    clicked,
    purchased,
    recommendation_context
) 
-- Generate 5000 random style similarity matches
SELECT 
    'MATCH_' || LPAD(generate_series::text, 6, '0') as match_id,
    (FLOOR(RANDOM() * 50000) + 1)::varchar as customer_id,
    (FLOOR(RANDOM() * 710) + 1)::varchar as product_id,
    ROUND((RANDOM() * 0.4 + 0.6)::numeric, 3) as similarity_score, -- Score between 0.6-1.0
    CASE 
        WHEN RANDOM() < 0.3 THEN 'style_based'
        WHEN RANDOM() < 0.6 THEN 'color_match'
        WHEN RANDOM() < 0.8 THEN 'trend_similar'
        ELSE 'brand_affinity'
    END as recommendation_type,
    NOW() - (RANDOM() * INTERVAL '90 days') as match_date,
    CASE WHEN RANDOM() < 0.15 THEN TRUE ELSE FALSE END as clicked, -- 15% click rate
    CASE WHEN RANDOM() < 0.03 THEN TRUE ELSE FALSE END as purchased, -- 3% purchase rate
    CASE 
        WHEN RANDOM() < 0.25 THEN 'homepage_recommendations'
        WHEN RANDOM() < 0.45 THEN 'product_page_similar'
        WHEN RANDOM() < 0.65 THEN 'cart_recommendations'
        WHEN RANDOM() < 0.80 THEN 'email_campaign'
        ELSE 'browse_history_based'
    END as recommendation_context
FROM generate_series(1, 5000);

-- Add some high-performing matches (clicked and purchased)
INSERT INTO style_similarity_matches (
    match_id,
    customer_id,
    product_id,
    similarity_score,
    recommendation_type,
    match_date,
    clicked,
    purchased,
    recommendation_context
) 
SELECT 
    'MATCH_' || LPAD((5000 + generate_series)::text, 6, '0') as match_id,
    (FLOOR(RANDOM() * 50000) + 1)::varchar as customer_id,
    (FLOOR(RANDOM() * 710) + 1)::varchar as product_id,
    ROUND((RANDOM() * 0.2 + 0.8)::numeric, 3) as similarity_score, -- Higher scores 0.8-1.0
    CASE 
        WHEN RANDOM() < 0.4 THEN 'style_based'
        WHEN RANDOM() < 0.7 THEN 'trend_similar'
        ELSE 'brand_affinity'
    END as recommendation_type,
    NOW() - (RANDOM() * INTERVAL '30 days') as match_date,
    TRUE as clicked, -- All clicked
    TRUE as purchased, -- All purchased
    CASE 
        WHEN RANDOM() < 0.4 THEN 'product_page_similar'
        WHEN RANDOM() < 0.7 THEN 'cart_recommendations'
        ELSE 'email_campaign'
    END as recommendation_context
FROM generate_series(1, 200);

-- Add some recent matches with no engagement
INSERT INTO style_similarity_matches (
    match_id,
    customer_id,
    product_id,
    similarity_score,
    recommendation_type,
    match_date,
    clicked,
    purchased,
    recommendation_context
) 
SELECT 
    'MATCH_' || LPAD((5200 + generate_series)::text, 6, '0') as match_id,
    (FLOOR(RANDOM() * 50000) + 1)::varchar as customer_id,
    (FLOOR(RANDOM() * 710) + 1)::varchar as product_id,
    ROUND((RANDOM() * 0.5 + 0.5)::numeric, 3) as similarity_score, -- Medium scores 0.5-1.0
    CASE 
        WHEN RANDOM() < 0.35 THEN 'style_based'
        WHEN RANDOM() < 0.60 THEN 'color_match'
        ELSE 'browse_history_based'
    END as recommendation_type,
    NOW() - (RANDOM() * INTERVAL '7 days') as match_date,
    FALSE as clicked,
    FALSE as purchased,
    CASE 
        WHEN RANDOM() < 0.5 THEN 'homepage_recommendations'
        ELSE 'email_campaign'
    END as recommendation_context
FROM generate_series(1, 800);