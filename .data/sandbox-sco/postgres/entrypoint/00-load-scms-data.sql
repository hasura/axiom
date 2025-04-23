--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Homebrew)

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
-- Name: us; Type: SCHEMA; Schema: -; Owner: user
--

CREATE SCHEMA us;


ALTER SCHEMA us OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: billofmaterials; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.billofmaterials (
    shoe_id integer NOT NULL,
    material_id integer NOT NULL,
    quantity_required numeric(10,2)
);


ALTER TABLE us.billofmaterials OWNER TO "user";

--
-- Name: factories; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.factories (
    factory_id integer NOT NULL,
    name character varying(100),
    location character varying(100),
    capacity integer
);


ALTER TABLE us.factories OWNER TO "user";

--
-- Name: factories_factory_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.factories_factory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.factories_factory_id_seq OWNER TO "user";

--
-- Name: factories_factory_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.factories_factory_id_seq OWNED BY us.factories.factory_id;


--
-- Name: productionorders; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.productionorders (
    order_id integer NOT NULL,
    shoe_id integer,
    factory_id integer,
    quantity integer,
    start_date date,
    expected_completion date
);


ALTER TABLE us.productionorders OWNER TO "user";

--
-- Name: productionorders_order_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.productionorders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.productionorders_order_id_seq OWNER TO "user";

--
-- Name: productionorders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.productionorders_order_id_seq OWNED BY us.productionorders.order_id;


--
-- Name: rawmaterials; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.rawmaterials (
    material_id integer NOT NULL,
    name character varying(100) NOT NULL,
    unit character varying(20),
    cost_per_unit numeric(10,2)
);


ALTER TABLE us.rawmaterials OWNER TO "user";

--
-- Name: rawmaterials_material_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.rawmaterials_material_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.rawmaterials_material_id_seq OWNER TO "user";

--
-- Name: rawmaterials_material_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.rawmaterials_material_id_seq OWNED BY us.rawmaterials.material_id;


--
-- Name: shipments; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.shipments (
    shipment_id integer NOT NULL,
    order_id integer,
    warehouse_id integer,
    shipped_date date,
    arrival_date date,
    quantity integer
);


ALTER TABLE us.shipments OWNER TO "user";

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.shipments_shipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.shipments_shipment_id_seq OWNER TO "user";

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.shipments_shipment_id_seq OWNED BY us.shipments.shipment_id;


--
-- Name: shoes; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.shoes (
    shoe_id integer NOT NULL,
    model_name character varying(100),
    category character varying(50),
    release_date date
);


ALTER TABLE us.shoes OWNER TO "user";

--
-- Name: shoes_shoe_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.shoes_shoe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.shoes_shoe_id_seq OWNER TO "user";

--
-- Name: shoes_shoe_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.shoes_shoe_id_seq OWNED BY us.shoes.shoe_id;


--
-- Name: suppliermaterials; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.suppliermaterials (
    supplier_id integer NOT NULL,
    material_id integer NOT NULL,
    lead_time_days integer
);


ALTER TABLE us.suppliermaterials OWNER TO "user";

--
-- Name: suppliers; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.suppliers (
    supplier_id integer NOT NULL,
    name character varying(100) NOT NULL,
    contact_email character varying(100),
    country character varying(50)
);


ALTER TABLE us.suppliers OWNER TO "user";

--
-- Name: suppliers_supplier_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.suppliers_supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.suppliers_supplier_id_seq OWNER TO "user";

--
-- Name: suppliers_supplier_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.suppliers_supplier_id_seq OWNED BY us.suppliers.supplier_id;


--
-- Name: warehouses; Type: TABLE; Schema: us; Owner: user
--

CREATE TABLE us.warehouses (
    warehouse_id integer NOT NULL,
    name character varying(100),
    location character varying(100)
);


ALTER TABLE us.warehouses OWNER TO "user";

--
-- Name: warehouses_warehouse_id_seq; Type: SEQUENCE; Schema: us; Owner: user
--

CREATE SEQUENCE us.warehouses_warehouse_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.warehouses_warehouse_id_seq OWNER TO "user";

--
-- Name: warehouses_warehouse_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: user
--

ALTER SEQUENCE us.warehouses_warehouse_id_seq OWNED BY us.warehouses.warehouse_id;


--
-- Name: factories factory_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.factories ALTER COLUMN factory_id SET DEFAULT nextval('us.factories_factory_id_seq'::regclass);


--
-- Name: productionorders order_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.productionorders ALTER COLUMN order_id SET DEFAULT nextval('us.productionorders_order_id_seq'::regclass);


--
-- Name: rawmaterials material_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.rawmaterials ALTER COLUMN material_id SET DEFAULT nextval('us.rawmaterials_material_id_seq'::regclass);


--
-- Name: shipments shipment_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.shipments ALTER COLUMN shipment_id SET DEFAULT nextval('us.shipments_shipment_id_seq'::regclass);


--
-- Name: shoes shoe_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.shoes ALTER COLUMN shoe_id SET DEFAULT nextval('us.shoes_shoe_id_seq'::regclass);


--
-- Name: suppliers supplier_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.suppliers ALTER COLUMN supplier_id SET DEFAULT nextval('us.suppliers_supplier_id_seq'::regclass);


--
-- Name: warehouses warehouse_id; Type: DEFAULT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.warehouses ALTER COLUMN warehouse_id SET DEFAULT nextval('us.warehouses_warehouse_id_seq'::regclass);


--
-- Data for Name: billofmaterials; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.billofmaterials (shoe_id, material_id, quantity_required) FROM stdin;
1	3	0.55
1	7	1.82
1	6	1.32
2	1	0.81
2	6	1.32
2	3	0.96
3	7	0.53
3	2	1.09
3	4	1.86
4	4	1.66
4	5	1.15
4	3	0.55
5	4	0.56
5	6	1.06
5	7	0.60
6	6	1.40
6	4	1.37
6	3	1.07
7	3	1.56
7	5	0.84
7	1	1.03
8	5	1.65
8	2	0.64
8	1	0.16
9	3	0.75
9	5	0.86
9	7	0.89
10	6	0.32
10	7	1.02
10	4	0.49
11	1	1.00
11	3	1.43
11	5	1.20
12	4	0.79
12	1	0.98
12	3	1.99
13	4	1.63
13	1	1.61
13	7	1.80
14	2	0.19
14	7	0.29
14	5	0.27
15	3	0.35
15	6	0.36
15	2	0.16
16	6	1.93
16	7	0.30
16	5	0.46
17	2	1.73
17	7	0.32
17	5	0.64
18	6	0.20
18	1	1.88
18	2	0.29
19	6	1.11
19	5	1.36
19	3	1.68
20	6	1.27
20	5	1.48
20	2	0.33
\.


--
-- Data for Name: factories; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.factories (factory_id, name, location, capacity) FROM stdin;
1	Matthews PLC	East Samantha	13457
2	Rivera, Anderson and Harris	West Jay	10738
3	Thompson-Sullivan	Lauramouth	12860
4	Harris LLC	Alexistown	18313
5	Mullen and Sons	Port Patrickchester	7083
\.


--
-- Data for Name: productionorders; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.productionorders (order_id, shoe_id, factory_id, quantity, start_date, expected_completion) FROM stdin;
1	20	2	4905	2024-09-05	2024-10-21
2	2	5	4808	2025-02-17	2025-04-08
3	18	3	2146	2024-04-24	2024-05-10
4	1	1	1114	2025-04-12	2025-05-31
5	12	3	2074	2024-06-28	2024-07-10
6	4	3	199	2024-05-22	2024-06-13
7	4	4	2876	2024-06-09	2024-07-29
8	18	1	1759	2025-02-02	2025-03-30
9	4	5	440	2025-03-22	2025-05-04
10	18	3	2221	2024-06-12	2024-06-27
11	12	4	1493	2024-07-06	2024-08-16
12	8	1	2926	2024-06-07	2024-07-22
13	12	4	4001	2025-01-02	2025-02-24
14	5	3	2428	2025-01-27	2025-03-19
15	3	3	3693	2024-10-17	2024-12-04
16	15	4	1396	2024-08-07	2024-08-27
17	10	3	1181	2025-02-10	2025-03-07
18	20	1	344	2025-03-28	2025-05-26
19	3	4	1235	2024-07-24	2024-09-10
20	7	3	495	2025-04-11	2025-05-31
21	3	4	1530	2025-04-05	2025-04-20
22	10	2	3344	2025-04-12	2025-05-14
23	14	2	4917	2025-04-18	2025-06-13
24	6	4	4255	2024-08-24	2024-09-07
25	17	2	4158	2025-03-13	2025-04-16
26	11	5	1143	2025-03-02	2025-04-21
27	5	4	3200	2025-04-02	2025-05-12
28	4	5	3702	2025-04-17	2025-05-18
29	1	3	3117	2024-08-08	2024-09-28
30	11	3	4174	2025-03-02	2025-04-27
31	15	5	3092	2024-05-07	2024-05-21
32	1	4	4894	2024-06-29	2024-07-23
33	16	1	4349	2024-10-21	2024-11-18
34	10	4	1808	2025-04-19	2025-06-05
35	11	1	3918	2024-07-29	2024-09-24
36	5	3	3880	2025-03-04	2025-04-06
37	14	3	121	2024-12-05	2025-01-21
38	9	5	3135	2024-05-17	2024-06-13
39	11	1	118	2025-02-16	2025-04-03
40	7	2	1417	2025-02-23	2025-03-16
41	17	3	355	2024-12-06	2025-01-25
42	10	4	4864	2025-01-06	2025-02-12
43	19	3	241	2024-06-28	2024-08-23
44	17	2	872	2024-04-21	2024-05-17
45	4	5	1427	2024-09-03	2024-10-30
46	8	4	778	2024-05-02	2024-06-08
47	9	4	3610	2025-02-10	2025-04-05
48	1	4	3889	2024-10-03	2024-11-13
49	13	2	3035	2025-01-09	2025-01-19
50	15	3	2206	2024-08-21	2024-09-25
51	17	5	2329	2024-10-06	2024-10-27
52	19	1	3350	2024-11-09	2024-11-28
53	15	5	853	2025-01-15	2025-02-22
54	2	5	433	2025-01-04	2025-01-14
55	17	5	3967	2024-12-30	2025-01-13
56	18	2	1767	2024-11-02	2024-12-15
57	10	4	3452	2024-06-02	2024-07-24
58	8	4	584	2024-08-19	2024-10-09
59	9	3	3081	2025-03-23	2025-05-08
60	7	2	1925	2024-06-16	2024-07-17
61	15	2	1419	2025-03-24	2025-04-24
62	10	2	1923	2024-06-30	2024-07-24
63	16	1	1438	2025-02-07	2025-03-08
64	3	5	4066	2025-03-12	2025-04-06
65	14	5	323	2024-09-06	2024-10-24
66	3	1	658	2024-12-12	2024-12-23
67	7	2	668	2025-02-11	2025-02-21
68	13	5	166	2024-10-28	2024-12-13
69	16	1	1754	2025-01-31	2025-02-20
70	19	2	4020	2024-11-02	2024-12-16
71	17	4	3825	2024-07-02	2024-08-16
72	2	4	1366	2024-07-21	2024-08-05
73	15	3	3755	2025-01-26	2025-03-10
74	10	3	4271	2024-09-04	2024-10-20
75	17	5	3836	2024-11-14	2025-01-06
76	13	4	634	2024-05-31	2024-07-14
77	18	3	1212	2025-01-01	2025-02-12
78	17	1	1784	2024-06-11	2024-07-25
79	15	1	4369	2024-04-27	2024-06-01
80	2	1	1674	2024-09-03	2024-11-02
81	1	4	931	2024-08-08	2024-08-18
82	4	3	4036	2025-01-01	2025-02-14
83	16	3	2096	2025-01-27	2025-02-06
84	7	5	4986	2025-02-21	2025-03-09
85	12	5	1642	2024-06-29	2024-07-14
86	13	4	1554	2025-01-22	2025-03-11
87	10	1	3567	2024-12-04	2025-02-02
88	1	4	2892	2025-04-03	2025-04-17
89	5	4	3307	2025-04-12	2025-06-07
90	5	2	184	2024-12-27	2025-01-27
91	10	1	3668	2025-03-22	2025-04-02
92	19	2	2587	2024-10-16	2024-11-02
93	7	4	3673	2024-11-02	2024-11-25
94	2	4	3103	2024-09-30	2024-10-14
95	13	4	3230	2024-12-11	2025-01-12
96	19	3	2750	2024-10-11	2024-11-02
97	6	5	274	2024-07-01	2024-08-04
98	10	4	3134	2024-05-31	2024-07-15
99	14	3	1689	2024-10-05	2024-11-17
100	10	5	2381	2024-11-04	2024-12-20
101	3	4	1730	2024-07-27	2024-08-07
102	3	2	4450	2024-05-07	2024-06-28
103	4	5	1993	2025-02-11	2025-03-26
104	4	4	3234	2024-06-18	2024-07-03
105	6	1	4261	2024-12-25	2025-02-01
106	6	1	3441	2024-05-07	2024-05-27
107	5	3	1300	2024-11-12	2025-01-06
108	17	4	489	2024-05-15	2024-06-02
109	6	1	3145	2024-05-02	2024-06-24
110	8	1	1569	2025-01-06	2025-02-22
111	19	4	759	2024-10-23	2024-12-05
112	5	3	899	2024-05-21	2024-07-09
113	13	4	2111	2024-05-19	2024-06-24
114	20	2	1177	2024-06-28	2024-07-19
115	16	2	2365	2025-01-03	2025-01-25
116	6	1	2562	2024-07-10	2024-07-20
117	15	3	3463	2024-11-03	2024-12-07
118	5	5	4816	2024-09-11	2024-10-26
119	9	2	4865	2024-10-25	2024-11-17
120	1	2	4893	2024-08-26	2024-10-02
121	12	3	4180	2024-07-01	2024-08-23
122	9	2	2226	2024-05-12	2024-06-25
123	19	2	1124	2024-09-04	2024-10-28
124	15	2	4266	2024-05-01	2024-06-06
125	20	5	2841	2024-06-08	2024-07-14
126	4	3	1491	2024-04-26	2024-05-09
127	11	2	3763	2024-06-06	2024-07-03
128	9	2	519	2025-04-01	2025-05-27
129	13	3	4355	2024-07-05	2024-08-20
130	2	5	2250	2024-08-24	2024-09-14
131	6	2	849	2024-04-22	2024-06-05
132	12	5	1268	2025-01-12	2025-02-21
133	9	4	350	2024-07-23	2024-09-14
134	4	4	2562	2024-12-08	2024-12-31
135	2	2	4314	2024-10-02	2024-11-23
136	4	1	2661	2024-06-24	2024-07-20
137	17	5	1568	2024-11-02	2024-11-12
138	2	2	709	2025-03-20	2025-05-06
139	16	4	2414	2024-05-09	2024-05-29
140	7	1	3289	2025-02-14	2025-03-30
141	3	4	1064	2024-08-15	2024-09-28
142	4	4	3659	2024-08-05	2024-09-12
143	9	2	1714	2024-11-06	2024-11-20
144	7	4	2474	2024-09-14	2024-11-08
145	17	4	105	2024-05-04	2024-06-29
146	17	5	1095	2024-12-31	2025-01-11
147	16	3	2940	2025-01-11	2025-03-04
148	20	1	4912	2025-03-12	2025-05-11
149	4	4	2874	2024-09-12	2024-10-15
150	9	3	3117	2024-12-09	2024-12-28
151	8	1	500	2025-04-21	2025-05-17
152	8	5	500	2025-04-21	2025-05-17
153	14	2	500	2025-04-21	2025-05-03
154	18	4	500	2025-04-21	2025-05-19
155	18	5	500	2025-04-21	2025-05-21
156	8	5	500	2025-04-21	2025-05-13
157	14	4	500	2025-04-21	2025-05-20
158	14	2	500	2025-04-21	2025-05-17
159	8	2	500	2025-04-21	2025-05-10
160	14	1	500	2025-04-21	2025-05-03
161	8	2	500	2025-04-21	2025-05-20
162	8	3	500	2025-04-21	2025-05-03
163	8	1	500	2025-04-21	2025-05-04
164	14	3	500	2025-04-21	2025-05-03
165	14	2	500	2025-04-21	2025-05-07
166	8	3	500	2025-04-21	2025-05-02
167	8	2	500	2025-04-21	2025-05-16
\.


--
-- Data for Name: rawmaterials; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.rawmaterials (material_id, name, unit, cost_per_unit) FROM stdin;
1	Rubber	kg	4.91
2	Leather	kg	5.23
3	Foam	kg	4.54
4	Mesh	kg	11.04
5	Glue	kg	15.31
6	Cotton	kg	4.87
7	Plastic	kg	9.09
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.shipments (shipment_id, order_id, warehouse_id, shipped_date, arrival_date, quantity) FROM stdin;
1	23	1	2024-10-21	2024-11-05	1592
2	44	2	2025-01-24	2025-02-06	252
3	36	2	2024-06-28	2024-07-11	609
4	17	3	2024-05-20	2024-05-30	1368
5	50	5	2024-11-03	2024-11-07	347
6	35	2	2025-02-25	2025-03-03	77
7	4	2	2024-10-07	2024-10-16	994
8	15	3	2024-08-27	2024-09-06	865
9	2	4	2024-12-19	2025-01-02	1145
10	30	3	2025-02-08	2025-02-09	1869
11	16	4	2024-07-04	2024-07-12	609
12	5	4	2024-08-19	2024-08-29	447
13	6	3	2024-07-20	2024-07-21	1090
14	37	1	2024-05-29	2024-06-02	292
15	44	5	2025-03-24	2025-03-27	1702
16	5	2	2024-05-09	2024-05-11	723
17	40	3	2025-02-03	2025-02-04	494
18	24	2	2025-02-19	2025-02-27	717
19	42	2	2024-11-22	2024-12-07	1860
20	25	4	2024-10-20	2024-10-27	197
21	27	4	2025-02-06	2025-02-10	1897
22	29	2	2025-01-26	2025-02-02	1688
23	29	4	2024-10-18	2024-10-21	939
24	29	4	2024-09-16	2024-09-17	183
25	6	4	2025-04-14	2025-04-22	337
26	50	3	2025-01-20	2025-01-29	710
27	38	4	2024-07-11	2024-07-15	554
28	35	1	2024-08-01	2024-08-12	1415
29	10	2	2025-03-27	2025-04-05	459
30	14	5	2024-09-28	2024-10-06	1807
31	2	1	2025-03-18	2025-03-29	1443
32	23	1	2024-12-26	2024-12-29	115
33	30	3	2024-06-10	2024-06-16	1596
34	19	1	2024-08-03	2024-08-10	189
35	1	3	2024-08-30	2024-09-14	1359
36	32	5	2024-05-10	2024-05-20	1104
37	10	5	2025-02-21	2025-02-25	196
38	37	1	2025-04-20	2025-04-29	407
39	50	2	2024-08-08	2024-08-16	292
40	20	5	2024-05-21	2024-06-04	111
41	11	1	2024-05-13	2024-05-20	51
42	9	2	2024-09-16	2024-09-21	756
43	1	2	2024-06-21	2024-06-29	55
44	14	5	2024-05-05	2024-05-06	1601
45	15	3	2024-11-05	2024-11-19	952
46	17	3	2024-04-29	2024-05-07	1117
47	7	2	2024-08-17	2024-08-19	878
48	16	1	2024-11-01	2024-11-16	688
49	7	2	2024-04-27	2024-04-30	569
50	3	5	2024-09-30	2024-10-02	1103
51	17	5	2025-03-08	2025-03-15	578
52	45	1	2024-12-27	2025-01-03	392
53	48	3	2024-08-01	2024-08-14	493
54	40	3	2024-08-21	2024-08-27	405
55	40	2	2024-09-09	2024-09-13	1134
56	50	2	2024-12-17	2024-12-28	1039
57	26	3	2024-08-06	2024-08-18	1133
58	42	2	2024-10-02	2024-10-03	1166
59	36	4	2025-01-04	2025-01-14	1900
60	45	1	2025-03-09	2025-03-20	1146
61	39	1	2025-03-18	2025-03-21	1142
62	27	5	2024-06-15	2024-06-20	1360
63	16	5	2024-11-08	2024-11-10	932
64	44	4	2024-05-22	2024-06-03	1779
65	3	2	2024-10-31	2024-11-07	1674
66	23	4	2024-07-02	2024-07-12	1254
67	47	5	2024-11-27	2024-11-30	1612
68	36	1	2025-02-23	2025-02-24	1318
69	4	3	2024-05-16	2024-05-26	1305
70	29	1	2025-03-03	2025-03-08	216
71	32	1	2025-02-14	2025-02-25	1876
72	38	5	2025-03-04	2025-03-19	935
73	15	3	2025-02-18	2025-02-22	106
74	43	3	2024-08-22	2024-09-03	1451
75	14	3	2024-04-26	2024-04-27	815
76	45	1	2025-04-01	2025-04-10	278
77	30	4	2024-04-24	2024-05-04	198
78	22	4	2024-11-28	2024-12-06	918
79	42	3	2024-11-12	2024-11-14	129
80	37	2	2024-07-28	2024-08-09	331
81	18	5	2024-05-21	2024-06-03	1572
82	38	3	2024-10-20	2024-10-27	1006
83	10	5	2024-04-26	2024-05-02	623
84	30	5	2024-09-13	2024-09-17	249
85	2	4	2024-05-28	2024-06-03	1228
86	42	2	2024-06-29	2024-07-06	967
87	47	3	2025-03-28	2025-04-10	1112
88	43	3	2025-03-08	2025-03-18	1350
89	3	3	2024-12-23	2024-12-28	1708
90	44	3	2024-08-12	2024-08-22	1032
91	2	3	2025-03-22	2025-03-25	1429
92	7	2	2025-02-13	2025-02-27	766
93	11	4	2024-10-02	2024-10-09	1534
94	41	2	2025-03-29	2025-04-12	668
95	17	5	2024-11-14	2024-11-26	397
96	49	4	2024-12-27	2025-01-03	1713
97	48	5	2024-11-12	2024-11-22	624
98	31	2	2024-11-28	2024-12-09	1877
99	50	4	2025-01-13	2025-01-14	1641
100	33	2	2024-05-23	2024-05-24	203
\.


--
-- Data for Name: shoes; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.shoes (shoe_id, model_name, category, release_date) FROM stdin;
1	Report Runner	Running	2025-04-16
2	Price Runner	Casual	2024-06-23
3	Light Runner	Casual	2024-10-19
4	Direction Runner	Hiking	2023-10-19
5	Customer Runner	Hiking	2024-01-01
6	Which Runner	Running	2024-02-05
7	Television Runner	Casual	2024-04-08
8	Program Runner	Running	2024-03-19
9	Husband Runner	Casual	2023-06-16
10	Box Runner	Casual	2023-12-25
11	Relate Runner	Hiking	2024-10-19
12	Show Runner	Hiking	2024-05-22
13	Analysis Runner	Running	2023-10-21
14	Foreign Runner	Hiking	2024-09-10
15	Language Runner	Hiking	2025-01-10
16	Hit Runner	Running	2024-07-23
17	Together Runner	Hiking	2025-04-04
18	Administration Runner	Hiking	2023-11-21
19	Attention Runner	Casual	2024-12-10
20	Couple Runner	Hiking	2025-03-10
\.


--
-- Data for Name: suppliermaterials; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.suppliermaterials (supplier_id, material_id, lead_time_days) FROM stdin;
2	4	13
10	3	26
1	3	21
6	2	7
3	4	18
9	3	17
3	6	25
5	7	19
9	5	5
5	3	26
5	5	25
7	6	6
8	6	9
3	3	30
2	5	28
2	6	5
3	7	11
10	7	21
4	3	22
8	1	25
3	1	30
4	4	25
6	3	9
7	7	3
7	3	17
10	6	25
7	4	24
4	5	28
3	2	8
5	6	16
4	2	10
8	5	23
9	1	3
1	7	19
1	4	14
7	5	11
9	4	18
5	4	23
9	7	9
6	7	6
3	5	6
2	3	22
5	1	6
4	6	11
9	6	15
4	7	17
7	2	25
10	2	20
6	6	15
\.


--
-- Data for Name: suppliers; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.suppliers (supplier_id, name, contact_email, country) FROM stdin;
1	James LLC	millslisa@allison.com	US
2	Hancock, Barnett and Clark	hlucas@thompson-lambert.biz	US
3	Norris LLC	bmoore@zimmerman-ellis.com	US
4	Parker Inc	hunter72@alexander.com	US
5	Williams, Warren and Smith	cheryl85@parker-porter.com	US
6	Murphy-Newman	ujohnson@jimenez.com	US
7	Mcdowell Group	jorgegarcia@goodman-carpenter.com	US
8	Valencia and Sons	gcastaneda@blake.com	US
9	Holder, Campbell and Cunningham	billybrown@rodriguez.com	US
10	Brandt LLC	jamessellers@palmer-johnson.net	US
11	Mcclain, Hicks and Jenkins	rking@alexander.info	US
12	Lee-Meadows	reginahughes@garcia.biz	US
13	Henry and Sons	jacobrobinson@lewis-hicks.com	US
14	Martin Ltd	vfarmer@jordan-reed.biz	US
15	Hunt and Sons	spencerjoshua@king.com	US
16	Fuller, Brooks and Ingram	amandadiaz@bell.com	US
17	Matthews Ltd	kathy71@walker-farley.com	US
18	Gordon-Deleon	barbertanya@logan.biz	US
19	Compton Inc	erivera@olson-cox.com	US
20	Collins Ltd	daniellegutierrez@shepherd-park.org	US
21	Rios-Hill	cpacheco@carroll-mata.com	US
22	King, Gonzalez and Bowman	amandahall@norman-lin.com	US
23	Young Inc	douglas51@obrien.com	US
24	Duncan Inc	shepherdbilly@rogers.info	US
25	Howard Ltd	rswanson@becker.com	US
26	Vega Ltd	alexandertaylor@richardson.info	US
27	Farmer-Scott	dustinfields@gregory-smith.info	US
28	Wilkerson, Dunn and Jefferson	finleysean@crawford.info	US
29	Little-Wilson	warnerstephen@parks-garcia.net	US
30	Cox, Washington and Murphy	joseph45@bird.biz	US
31	Sosa, Castillo and Rasmussen	kevin40@fletcher-adams.com	US
32	Gonzalez LLC	luke44@barrett.com	US
33	Gardner, Murray and Carson	velazquezmegan@murphy.com	US
34	Rivas PLC	jason23@rios.com	US
35	Gates, Palmer and Jensen	seancarter@miller.org	US
36	Avery and Sons	bradharrington@kirk.info	US
37	Hughes-Freeman	susanwood@walker.com	US
38	Smith-Webster	wdean@harrington-dean.com	US
39	Hanson-Lee	jeffrey16@curry.com	US
40	Pena-Stafford	igutierrez@torres.com	US
\.


--
-- Data for Name: warehouses; Type: TABLE DATA; Schema: us; Owner: user
--

COPY us.warehouses (warehouse_id, name, location) FROM stdin;
1	Shepard, Carroll and Robertson	West Christopherbury
2	Frank, Barnes and Bailey	North Amy
3	Odom-Chang	Jonesside
4	Fox, Davidson and Jones	Jackfort
5	Frye-Martin	East Johnville
\.


--
-- Name: factories_factory_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.factories_factory_id_seq', 5, true);


--
-- Name: productionorders_order_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.productionorders_order_id_seq', 167, true);


--
-- Name: rawmaterials_material_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.rawmaterials_material_id_seq', 7, true);


--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.shipments_shipment_id_seq', 100, true);


--
-- Name: shoes_shoe_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.shoes_shoe_id_seq', 20, true);


--
-- Name: suppliers_supplier_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.suppliers_supplier_id_seq', 40, true);


--
-- Name: warehouses_warehouse_id_seq; Type: SEQUENCE SET; Schema: us; Owner: user
--

SELECT pg_catalog.setval('us.warehouses_warehouse_id_seq', 5, true);


--
-- Name: billofmaterials billofmaterials_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.billofmaterials
    ADD CONSTRAINT billofmaterials_pkey PRIMARY KEY (shoe_id, material_id);


--
-- Name: factories factories_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.factories
    ADD CONSTRAINT factories_pkey PRIMARY KEY (factory_id);


--
-- Name: productionorders productionorders_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.productionorders
    ADD CONSTRAINT productionorders_pkey PRIMARY KEY (order_id);


--
-- Name: rawmaterials rawmaterials_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.rawmaterials
    ADD CONSTRAINT rawmaterials_pkey PRIMARY KEY (material_id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (shipment_id);


--
-- Name: shoes shoes_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.shoes
    ADD CONSTRAINT shoes_pkey PRIMARY KEY (shoe_id);


--
-- Name: suppliermaterials suppliermaterials_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.suppliermaterials
    ADD CONSTRAINT suppliermaterials_pkey PRIMARY KEY (supplier_id, material_id);


--
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id);


--
-- Name: warehouses warehouses_pkey; Type: CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.warehouses
    ADD CONSTRAINT warehouses_pkey PRIMARY KEY (warehouse_id);


--
-- Name: billofmaterials billofmaterials_material_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.billofmaterials
    ADD CONSTRAINT billofmaterials_material_id_fkey FOREIGN KEY (material_id) REFERENCES us.rawmaterials(material_id);


--
-- Name: billofmaterials billofmaterials_shoe_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.billofmaterials
    ADD CONSTRAINT billofmaterials_shoe_id_fkey FOREIGN KEY (shoe_id) REFERENCES us.shoes(shoe_id);


--
-- Name: productionorders productionorders_factory_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.productionorders
    ADD CONSTRAINT productionorders_factory_id_fkey FOREIGN KEY (factory_id) REFERENCES us.factories(factory_id);


--
-- Name: productionorders productionorders_shoe_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.productionorders
    ADD CONSTRAINT productionorders_shoe_id_fkey FOREIGN KEY (shoe_id) REFERENCES us.shoes(shoe_id);


--
-- Name: shipments shipments_order_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.shipments
    ADD CONSTRAINT shipments_order_id_fkey FOREIGN KEY (order_id) REFERENCES us.productionorders(order_id);


--
-- Name: shipments shipments_warehouse_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.shipments
    ADD CONSTRAINT shipments_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES us.warehouses(warehouse_id);


--
-- Name: suppliermaterials suppliermaterials_material_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.suppliermaterials
    ADD CONSTRAINT suppliermaterials_material_id_fkey FOREIGN KEY (material_id) REFERENCES us.rawmaterials(material_id);


--
-- Name: suppliermaterials suppliermaterials_supplier_id_fkey; Type: FK CONSTRAINT; Schema: us; Owner: user
--

ALTER TABLE ONLY us.suppliermaterials
    ADD CONSTRAINT suppliermaterials_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES us.suppliers(supplier_id);


--
-- PostgreSQL database dump complete
--

