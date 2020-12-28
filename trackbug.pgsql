--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment (
    c_id integer NOT NULL,
    t_id integer,
    users_id integer,
    date character varying,
    comment character varying
);


ALTER TABLE public.comment OWNER TO postgres;

--
-- Name: comment_c_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comment_c_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_c_id_seq OWNER TO postgres;

--
-- Name: comment_c_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comment_c_id_seq OWNED BY public.comment.c_id;


--
-- Name: map_users_proj; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.map_users_proj (
    map_id integer NOT NULL,
    p_id integer,
    users_id integer,
    users_role character varying,
    users_assign_date character varying,
    users_end_date character varying
);


ALTER TABLE public.map_users_proj OWNER TO postgres;

--
-- Name: map_users_proj_map_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.map_users_proj_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_users_proj_map_id_seq OWNER TO postgres;

--
-- Name: map_users_proj_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.map_users_proj_map_id_seq OWNED BY public.map_users_proj.map_id;


--
-- Name: month_config; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.month_config (
    id integer NOT NULL,
    mth_id integer,
    mth_name character varying,
    mth_year integer
);


ALTER TABLE public.month_config OWNER TO postgres;

--
-- Name: month_config_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.month_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.month_config_id_seq OWNER TO postgres;

--
-- Name: month_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.month_config_id_seq OWNED BY public.month_config.id;


--
-- Name: notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification (
    n_id integer NOT NULL,
    t_id integer,
    users_id integer,
    type character varying
);


ALTER TABLE public.notification OWNER TO postgres;

--
-- Name: notification_n_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_n_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_n_id_seq OWNER TO postgres;

--
-- Name: notification_n_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_n_id_seq OWNED BY public.notification.n_id;


--
-- Name: project; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project (
    p_id integer NOT NULL,
    p_name character varying,
    p_desc character varying,
    p_start_date character varying,
    p_end_date character varying
);


ALTER TABLE public.project OWNER TO postgres;

--
-- Name: project_p_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_p_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_p_id_seq OWNER TO postgres;

--
-- Name: project_p_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_p_id_seq OWNED BY public.project.p_id;


--
-- Name: ticket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticket (
    t_id integer NOT NULL,
    t_title character varying,
    t_desc character varying,
    users_id integer,
    submitter_email character varying,
    p_id integer,
    t_priority character varying,
    t_status character varying,
    t_type character varying,
    t_create_date character varying,
    t_close_date character varying
);


ALTER TABLE public.ticket OWNER TO postgres;

--
-- Name: ticket_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticket_history (
    id integer NOT NULL,
    t_id integer,
    users_id integer,
    t_status character varying,
    t_update_date character varying,
    priority character varying
);


ALTER TABLE public.ticket_history OWNER TO postgres;

--
-- Name: ticket_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ticket_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ticket_history_id_seq OWNER TO postgres;

--
-- Name: ticket_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ticket_history_id_seq OWNED BY public.ticket_history.id;


--
-- Name: ticket_t_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ticket_t_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ticket_t_id_seq OWNER TO postgres;

--
-- Name: ticket_t_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ticket_t_id_seq OWNED BY public.ticket.t_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    users_id integer NOT NULL,
    users_email character varying,
    users_name character varying,
    users_password character varying,
    users_role character varying,
    update_date character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_users_id_seq OWNER TO postgres;

--
-- Name: users_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_users_id_seq OWNED BY public.users.users_id;


--
-- Name: comment c_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment ALTER COLUMN c_id SET DEFAULT nextval('public.comment_c_id_seq'::regclass);


--
-- Name: map_users_proj map_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.map_users_proj ALTER COLUMN map_id SET DEFAULT nextval('public.map_users_proj_map_id_seq'::regclass);


--
-- Name: month_config id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.month_config ALTER COLUMN id SET DEFAULT nextval('public.month_config_id_seq'::regclass);


--
-- Name: notification n_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification ALTER COLUMN n_id SET DEFAULT nextval('public.notification_n_id_seq'::regclass);


--
-- Name: project p_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project ALTER COLUMN p_id SET DEFAULT nextval('public.project_p_id_seq'::regclass);


--
-- Name: ticket t_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket ALTER COLUMN t_id SET DEFAULT nextval('public.ticket_t_id_seq'::regclass);


--
-- Name: ticket_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket_history ALTER COLUMN id SET DEFAULT nextval('public.ticket_history_id_seq'::regclass);


--
-- Name: users users_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN users_id SET DEFAULT nextval('public.users_users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
7dce91551da6
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comment (c_id, t_id, users_id, date, comment) FROM stdin;
1	1	8	7/1/2020	sam assigned to this ticket
2	1	9	9/1/2020	status changed to in-progess by sam
3	1	9	20/1/2020	Status changed to closed by sam
4	2	6	27/1/2020	cap assigned to this ticket
5	2	8	2/2/2020	status changed to in-progess by cap
6	2	8	30/4/2020	Status changed to closed by cap
7	3	6	27/2/2020	sam assigned to this ticket
8	3	9	2/3/2020	status changed to in-progess by sam
9	3	9	30/5/2020	Status changed to closed by sam
10	4	6	27/2/2020	sam assigned to this ticket
11	4	9	2/3/2020	status changed to in-progess
12	4	9	30/5/2020	Status changed to closed
13	5	6	27/2/2020	sam assigned to this ticket
14	5	9	2/3/2020	status changed to in-progess
15	5	9	30/5/2020	Status changed to closed
16	6	6	27/3/2020	cap assigned to this ticket
17	6	8	2/4/2020	status changed to in-progess
18	6	8	12/5/2020	Status changed to closed
19	7	6	30/3/2020	cap assigned to this ticket
20	7	8	2/4/2020	status changed to in-progess
21	7	8	12/5/2020	Status changed to closed
22	8	6	30/4/2020	adam assigned to this ticket
23	8	13	2/5/2020	status changed to in-progess
24	8	13	12/5/2020	Status changed to closed
25	9	6	30/4/2020	adam assigned to this ticket
26	9	13	2/5/2020	status changed to in-progess
27	9	13	12/5/2020	Status changed to closed
28	10	6	30/4/2020	adam assigned to this ticket
29	10	13	2/5/2020	status changed to in-progess
30	10	13	12/5/2020	Status changed to closed
31	11	6	30/5/2020	adam assigned to this ticket
32	11	13	2/6/2020	status changed to in-progess
33	11	13	12/6/2020	Status changed to closed
34	12	6	30/6/2020	adam assigned to this ticket
35	12	13	2/9/2020	status changed to in-progess
36	12	13	12/9/2020	Status changed to closed
37	13	6	30/6/2020	adam assigned to this ticket
38	13	13	2/9/2020	status changed to in-progess
39	13	13	12/9/2020	Status changed to closed
40	14	6	30/4/2020	cap assigned to this ticket
41	14	8	2/5/2020	status changed to in-progess
42	14	8	12/6/2020	Status changed to closed
43	15	6	24/11/2020	alice assigned to this ticket
44	15	11	25/11/2020	status changed to in-progess
45	15	11	25/11/2020	Status changed to closed
46	16	6	1/12/2020	alice assigned to this ticket
47	16	11	2/12/2020	status changed to in-progess
48	16	11	3/12/2020	Status changed to closed
49	17	6	3/12/2020	bob assigned to this ticket
50	17	10	3/12/2020	status changed to in-progess
51	17	10	4/12/2020	Status changed to closed
52	18	6	6/12/2020	bob assigned to this ticket
53	18	10	6/12/2020	status changed to in-progess
54	18	10	8/12/2020	Status changed to closed
55	19	6	18/12/2020	bob assigned to this ticket
56	19	10	19/12/2020	status changed to in-progess
57	19	10	20/12/2020	Status changed to closed
58	20	11	21/12/2020	bob assigned to this ticket
59	20	10	22/12/2020	status changed to in-progess
60	20	10	25/12/2020	Status changed to closed
\.


--
-- Data for Name: map_users_proj; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.map_users_proj (map_id, p_id, users_id, users_role, users_assign_date, users_end_date) FROM stdin;
1	1	6	manager	27/12/2020	N/A
2	2	6	manager	27/12/2020	N/A
3	3	6	manager	27/12/2020	N/A
4	4	7	manager	27/12/2020	N/A
5	1	8	dev	27/12/2020	N/A
6	1	9	dev	27/12/2020	N/A
7	2	10	dev	27/12/2020	N/A
8	2	11	dev	27/12/2020	N/A
9	2	12	dev	27/12/2020	N/A
10	3	13	dev	27/12/2020	N/A
11	3	14	dev	27/12/2020	N/A
12	4	15	dev	27/12/2020	N/A
13	4	16	dev	27/12/2020	N/A
14	4	17	dev	27/12/2020	N/A
16	1	2	user	27/12/2020	N/A
19	3	4	user	27/12/2020	N/A
20	4	5	user	27/12/2020	N/A
21	2	5	user	27/12/2020	N/A
18	2	3	user	27/12/2020	N/A
\.


--
-- Data for Name: month_config; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.month_config (id, mth_id, mth_name, mth_year) FROM stdin;
1	1	Jan`20	2020
2	2	Feb`20	2020
3	3	Mar`20	2020
4	4	Apr`20	2020
5	5	May`20	2020
6	6	Jun`20	2020
7	7	Jul`20	2020
8	8	Aug`20	2020
9	9	Sep`20	2020
10	10	Oct`20	2020
11	11	Nov`20	2020
12	12	Dec`20	2020
13	1	Jan`21	2021
14	2	Feb`21	2021
15	3	Mar`21	2021
16	4	Apr`21	2021
17	5	May`21	2021
18	6	Jun`21	2021
19	7	Jul`21	2021
20	8	Aug`21	2021
21	9	Sep`21	2021
22	10	Oct`21	2021
23	11	Nov`21	2021
24	12	Dec`21	2021
\.


--
-- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification (n_id, t_id, users_id, type) FROM stdin;
1	1	6	new
2	1	8	new
3	1	9	new
4	1	2	new
5	1	9	assigned
6	1	6	update
7	1	8	update
8	1	9	update
9	1	2	update
10	1	6	update
11	1	8	update
12	1	9	update
13	1	2	update
14	2	9	assigned
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project (p_id, p_name, p_desc, p_start_date, p_end_date) FROM stdin;
1	HandWritten digits recognition	Use a CNN model to recognize digits from 0 to 9	1/1/2020	N/A
2	Bug Tracker	Use python-flask and postgreSql to implement bugTracker	1/1/2020	N/A
3	Tapestry algorithm Simulator 	Routing algorithm for decentralized distributed systems for object location and routing	1/1/2020	N/A
4	Data Deduplication on cloud storage	Use hash-table based File compression algorithm to deduplicate data	1/1/2020	N/A
\.


--
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ticket (t_id, t_title, t_desc, users_id, submitter_email, p_id, t_priority, t_status, t_type, t_create_date, t_close_date) FROM stdin;
1	Graph not accurate	The accuracy vs data graph has error at the dates after DEC	9	alice@gmail.com	1	Low	closed	Error	4/1/2020	20/1/2020
3	Graph not displayed	data is passed from the backend, some frontend issuse	9	user1@gmail.com	1	Low	closed	error	8/2/2020	30/5/2020
4	Time not correct	Exectuion time value is in seconds, convert to milliseconds	9	user1@gmail.com	1	High	closed	error	8/2/2020	30/5/2020
5	numpy not compatible	Need to change the numpy version, not compatible	9	user1@gmail.com	1	Medium	closed	error	8/2/2020	30/5/2020
6	Download from colab	code not woring on local machine	8	user1@gmail.com	1	Low	closed	error	8/2/2020	12/5/2020
7	Accuracy very less	after adding new data accuracy decreased	8	user1@gmail.com	1	High	closed	fix	8/3/2020	12/5/2020
8	star network wrong	Every distributed system not correctly attached	13	user3@gmail.com	3	Low	closed	error	9/4/2020	12/5/2020
9	Data file corrupted	system 3 has wrong data file	13	user3@gmail.com	3	High	closed	error	9/4/2020	12/5/2020
10	Routing not working	The routing table update function is wrong	13	user3@gmail.com	3	High	closed	error	9/4/2020	12/5/2020
11	Router Table courrpted	The routing table update function is wrong	13	user3@gmail.com	3	Medium	closed	error	9/5/2020	12/6/2020
12	Dead node error	The dead node not removed from router tables	13	user3@gmail.com	3	Low	closed	error	9/6/2020	12/9/2020
13	Slow execution	Node 3 taking too long to process and forward the message	13	user3@gmail.com	3	High	closed	error	9/6/2020	12/9/2020
14	too long execution time	Node 3 taking too long to process and forward the message	8	user1@gmail.com	1	Low	closed	error	9/4/2020	12/6/2020
15	Ticket list displays projectID	Display Project name instead of ID, correct the sql query	11	user2@gmail.com	2	Medium	closed	error	24/11/2020	25/11/2020
16	Callback URL not returning user role	Implement a new table to store the user authorization details	11	user2@gmail.com	2	Low	closed	bug	1/12/2020	3/12/2020
17	Developer cant change ticket status	Implement a new endpoint, to make developer change status	10	user4@gmail.com	2	Medium	closed	bug	2/12/2020	4/12/2020
18	Delete notification	Delete a notification after clicking on it	10	user4@gmail.com	2	High	closed	bug	5/12/2020	8/12/2020
19	Admin create project error	admin endpoint failed to create new projects	10	user4@gmail.com	2	High	closed	bug	18/12/2020	20/12/2020
20	Error while removing manager	Admin cant remove managers from project	10	user4@gmail.com	2	Medium	closed	bug	21/12/2020	25/12/2020
2	Accuracy issuse	The accuracy for unseen data below 30	9	user1@gmail.com	1	Low	closed	error	8/1/2020	30/4/2020
\.


--
-- Data for Name: ticket_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ticket_history (id, t_id, users_id, t_status, t_update_date, priority) FROM stdin;
1	1	0	open	4/1/2020	Low
2	1	9	open	7/1/2020	Low
3	1	9	in-progress	9/1/2020	Low
4	1	9	closed	20/1/2020	Low
5	2	0	open	8/1/2020	Low
6	2	8	open	27/1/2020	Low
7	2	8	in-progress	2/2/2020	Low
8	2	8	closed	30/4/2020	Low
9	3	0	open	8/2/2020	Low
10	3	9	open	27/2/2020	Low
11	3	9	in-progress	2/3/2020	Low
12	3	9	closed	30/5/2020	Low
13	4	0	open	8/2/2020	High
14	4	9	open	27/2/2020	High
15	4	9	in-progress	2/3/2020	High
16	4	9	closed	30/5/2020	High
17	5	0	open	8/2/2020	Medium
18	5	9	open	27/2/2020	Medium
19	5	9	in-progress	2/3/2020	Medium
20	5	9	closed	30/5/2020	Medium
21	6	0	open	8/2/2020	Low
22	6	8	open	27/3/2020	Low
23	6	8	in-progress	2/4/2020	Low
24	6	8	closed	12/5/2020	Low
25	7	0	open	8/3/2020	High
26	7	8	open	30/3/2020	High
27	7	8	in-progress	2/4/2020	High
28	7	8	closed	12/5/2020	High
29	8	0	open	9/4/2020	Low
30	8	13	open	30/4/2020	Low
31	8	13	in-progress	2/5/2020	Low
32	8	13	closed	12/5/2020	Low
33	9	0	open	9/4/2020	High
34	9	13	open	30/4/2020	High
35	9	13	in-progress	2/5/2020	High
36	9	13	closed	12/5/2020	High
37	10	0	open	9/4/2020	High
38	10	13	open	30/4/2020	High
39	10	13	in-progress	2/5/2020	High
40	10	13	closed	12/5/2020	High
41	11	0	open	9/5/2020	Medium
42	11	13	open	30/5/2020	Medium
43	11	13	in-progress	2/6/2020	Medium
44	11	13	closed	12/6/2020	Medium
45	12	0	open	9/6/2020	Low
46	12	13	open	30/6/2020	Low
47	12	13	in-progress	2/9/2020	Low
48	12	13	closed	12/9/2020	Low
49	13	0	open	9/6/2020	High
50	13	13	open	30/6/2020	High
51	13	13	in-progress	2/9/2020	High
52	13	13	closed	12/9/2020	High
53	14	0	open	9/4/2020	Low
54	14	8	open	30/4/2020	Low
55	14	8	in-progress	2/5/2020	Low
56	14	8	closed	12/6/2020	Low
57	15	0	open	24/11/2020	Medium
58	15	11	open	24/11/2020	Medium
59	15	11	in-progress	25/11/2020	Medium
60	15	11	closed	25/11/2020	Medium
61	16	0	open	1/12/2020	Low
62	16	11	open	1/12/2020	Low
63	16	11	in-progress	2/12/2020	Low
64	16	11	closed	3/12/2020	Low
65	17	0	open	2/12/2020	Medium
66	17	10	open	3/12/2020	Medium
67	17	10	in-progress	3/12/2020	Medium
68	17	10	closed	4/12/2020	Medium
69	18	0	open	5/12/2020	High
70	18	10	open	6/12/2020	High
71	18	10	in-progress	6/12/2020	High
72	18	10	closed	8/12/2020	High
73	19	0	open	18/12/2020	High
74	19	10	open	18/12/2020	High
75	19	10	in-progress	19/12/2020	High
76	19	10	closed	20/12/2020	High
77	20	0	open	21/12/2020	Medium
78	20	10	open	21/12/2020	Medium
79	20	10	in-progress	22/12/2020	Medium
80	20	10	closed	25/12/2020	Medium
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (users_id, users_email, users_name, users_password, users_role, update_date) FROM stdin;
1	admin@gmail.com	admin	admin	admin	1/1/2020
8	cap@gmail.com	cap	cap	dev	27/12/2020
9	sam@gmail.com	sam	sam	dev	27/12/2020
10	bob@gmail.com	bob	bob	dev	27/12/2020
11	alice@gmail.com	alice	alice	dev	27/12/2020
3	user2@gmail.com	user2	user2	user	27/12/2020
4	user3@gmail.com	user3	user3	user	27/12/2020
5	user4@gmail.com	user4	user4	user	27/12/2020
2	user1@gmail.com	user1	user1	user	27/12/2020
6	manager1@gmail.com	manager1	manager1	manager	27/12/2020
7	manager2@gmail.com	manager2	manager2	manager	27/12/2020
12	josh@gmail.com	josh	josh	dev	27/12/2020
13	adam@gmail.com	adam	adam	dev	27/12/2020
14	eve@gmail.com	eve	eve	dev	27/12/2020
15	grace@gmail.com	grace	grace	dev	27/12/2020
16	cole@gmail.com	cole	cole	dev	27/12/2020
17	jane@gmail.com	jane	jane	dev	27/12/2020
\.


--
-- Name: comment_c_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comment_c_id_seq', 4, true);


--
-- Name: map_users_proj_map_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.map_users_proj_map_id_seq', 23, true);


--
-- Name: month_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.month_config_id_seq', 1, false);


--
-- Name: notification_n_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notification_n_id_seq', 14, true);


--
-- Name: project_p_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_p_id_seq', 1, false);


--
-- Name: ticket_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ticket_history_id_seq', 4, true);


--
-- Name: ticket_t_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ticket_t_id_seq', 1, false);


--
-- Name: users_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_users_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (c_id);


--
-- Name: map_users_proj map_users_proj_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.map_users_proj
    ADD CONSTRAINT map_users_proj_pkey PRIMARY KEY (map_id);


--
-- Name: month_config month_config_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.month_config
    ADD CONSTRAINT month_config_pkey PRIMARY KEY (id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (n_id);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (p_id);


--
-- Name: ticket_history ticket_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket_history
    ADD CONSTRAINT ticket_history_pkey PRIMARY KEY (id);


--
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (t_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (users_id);


--
-- PostgreSQL database dump complete
--

