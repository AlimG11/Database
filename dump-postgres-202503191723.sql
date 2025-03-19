--
-- PostgreSQL database cluster dump
--

-- Started on 2025-03-19 17:23:41

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 17rc1
-- Dumped by pg_dump version 17rc1

-- Started on 2025-03-19 17:23:41

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

-- Completed on 2025-03-19 17:23:42

--
-- PostgreSQL database dump complete
--

--
-- Database "market" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17rc1
-- Dumped by pg_dump version 17rc1

-- Started on 2025-03-19 17:23:42

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
-- TOC entry 4877 (class 1262 OID 16388)
-- Name: market; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE market WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';


ALTER DATABASE market OWNER TO postgres;

\connect market

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 24577)
-- Name: product_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_categories (
    category_id integer NOT NULL,
    category_name character varying(64) NOT NULL
);


ALTER TABLE public.product_categories OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24576)
-- Name: product_categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_categories_category_id_seq OWNER TO postgres;

--
-- TOC entry 4878 (class 0 OID 0)
-- Dependencies: 218
-- Name: product_categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_categories_category_id_seq OWNED BY public.product_categories.category_id;


--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24587)
-- Name: purchase_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.purchase_history (
    purchase_id integer NOT NULL,
    client_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    purchase_date date,
    total_price numeric(10,2) NOT NULL
);


ALTER TABLE public.purchase_history OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24586)
-- Name: purchase_history_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.purchase_history_purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purchase_history_purchase_id_seq OWNER TO postgres;

--
-- TOC entry 4879 (class 0 OID 0)
-- Dependencies: 220
-- Name: purchase_history_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.purchase_history_purchase_id_seq OWNED BY public.purchase_history.purchase_id;


--
-- TOC entry 223 (class 1259 OID 24594)
-- Name: supply_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supply_history (
    supply_id integer NOT NULL,
    seller_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    date_of_update date
);


ALTER TABLE public.supply_history OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 24593)
-- Name: supply_history_supply_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.supply_history_supply_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.supply_history_supply_id_seq OWNER TO postgres;

--
-- TOC entry 4880 (class 0 OID 0)
-- Dependencies: 222
-- Name: supply_history_supply_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.supply_history_supply_id_seq OWNED BY public.supply_history.supply_id;


--
-- TOC entry 4709 (class 2604 OID 24580)
-- Name: product_categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories ALTER COLUMN category_id SET DEFAULT nextval('public.product_categories_category_id_seq'::regclass);


--
-- TOC entry 4710 (class 2604 OID 24590)
-- Name: purchase_history purchase_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_history ALTER COLUMN purchase_id SET DEFAULT nextval('public.purchase_history_purchase_id_seq'::regclass);


--
-- TOC entry 4711 (class 2604 OID 24597)
-- Name: supply_history supply_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supply_history ALTER COLUMN supply_id SET DEFAULT nextval('public.supply_history_supply_id_seq'::regclass);


--
-- TOC entry 4867 (class 0 OID 24577)
-- Dependencies: 219
-- Data for Name: product_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_categories (category_id, category_name) FROM stdin;
\.


--
-- TOC entry 4865 (class 0 OID 16389)
-- Dependencies: 217
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products  FROM stdin;
\.


--
-- TOC entry 4869 (class 0 OID 24587)
-- Dependencies: 221
-- Data for Name: purchase_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.purchase_history (purchase_id, client_id, product_id, quantity, purchase_date, total_price) FROM stdin;
\.


--
-- TOC entry 4871 (class 0 OID 24594)
-- Dependencies: 223
-- Data for Name: supply_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.supply_history (supply_id, seller_id, product_id, quantity, date_of_update) FROM stdin;
\.


--
-- TOC entry 4881 (class 0 OID 0)
-- Dependencies: 218
-- Name: product_categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_categories_category_id_seq', 1, false);


--
-- TOC entry 4882 (class 0 OID 0)
-- Dependencies: 220
-- Name: purchase_history_purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.purchase_history_purchase_id_seq', 1, false);


--
-- TOC entry 4883 (class 0 OID 0)
-- Dependencies: 222
-- Name: supply_history_supply_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.supply_history_supply_id_seq', 1, false);


--
-- TOC entry 4713 (class 2606 OID 24584)
-- Name: product_categories product_categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_category_name_key UNIQUE (category_name);


--
-- TOC entry 4715 (class 2606 OID 24582)
-- Name: product_categories product_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_pkey PRIMARY KEY (category_id);


--
-- TOC entry 4717 (class 2606 OID 24592)
-- Name: purchase_history purchase_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_history
    ADD CONSTRAINT purchase_history_pkey PRIMARY KEY (purchase_id);


--
-- TOC entry 4719 (class 2606 OID 24599)
-- Name: supply_history supply_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supply_history
    ADD CONSTRAINT supply_history_pkey PRIMARY KEY (supply_id);


-- Completed on 2025-03-19 17:23:42

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 17rc1
-- Dumped by pg_dump version 17rc1

-- Started on 2025-03-19 17:23:42

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
-- TOC entry 227 (class 1255 OID 24713)
-- Name: calculate_total_price(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.calculate_total_price() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	-- Устанавливаем цену из таблицы products
    SELECT p.price INTO NEW.price
    FROM products p
    WHERE p.product_id = NEW.product_id;

    -- Если товара нет, выбрасываем ошибку
    IF NEW.price IS NULL THEN
        RAISE EXCEPTION 'Товар с ID % не найден в products!', NEW.product_id;
    END IF;

    NEW.total_price = NEW.price * NEW.quantity;
	RETURN NEW;
END;
$$;


ALTER FUNCTION public.calculate_total_price() OWNER TO postgres;

--
-- TOC entry 228 (class 1255 OID 24732)
-- Name: check_add_categories(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_add_categories() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Проверяем является ли пользователь клиентом
	IF (SELECT user_role FROM users WHERE user_id = NEW.seller_id) = 'client' THEN
        RAISE EXCEPTION 'Добавлять новые категории товара могут только продавцы!';
    END IF;

	RETURN NEW;
END;
$$;


ALTER FUNCTION public.check_add_categories() OWNER TO postgres;

--
-- TOC entry 241 (class 1255 OID 24716)
-- Name: update_quantity_on_purchase(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_quantity_on_purchase() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	-- Проверяем является ли пользователь продавцом
	IF (SELECT user_role FROM users WHERE user_id = NEW.client_id) = 'seller' THEN
        RAISE EXCEPTION 'Покупать товар могут только клиенты!';
    END IF;

    -- Проверяем, есть ли нужное количество товара на складе
    IF (SELECT total_quantity FROM products WHERE product_id = NEW.product_id) < NEW.quantity THEN
        RAISE EXCEPTION 'Недостаточно товара на складе!';
    END IF;

    -- Уменьшаем количество доступного товара и обновляем дату
    UPDATE products
    SET total_quantity = total_quantity - NEW.quantity,
		date_of_update = CURRENT_DATE
    WHERE product_id = NEW.product_id;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_quantity_on_purchase() OWNER TO postgres;

--
-- TOC entry 240 (class 1255 OID 24718)
-- Name: update_quantity_on_supply(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_quantity_on_supply() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	-- Проверяем является ли пользователь клиентом
	IF (SELECT user_role FROM users WHERE user_id = NEW.seller_id) = 'client' THEN
        RAISE EXCEPTION 'Поставлять товар могут только продавцы!';
    END IF;

    -- Увеличиваем количество доступного товара и обновляем дату
    UPDATE products
    SET total_quantity = total_quantity + NEW.quantity,
		date_of_update = CURRENT_DATE
    WHERE product_id = NEW.product_id;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_quantity_on_supply() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 24641)
-- Name: product_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_categories (
    category_id integer NOT NULL,
    category_name character varying(64) NOT NULL,
    seller_id integer
);


ALTER TABLE public.product_categories OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24640)
-- Name: product_categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_categories_category_id_seq OWNER TO postgres;

--
-- TOC entry 4915 (class 0 OID 0)
-- Dependencies: 223
-- Name: product_categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_categories_category_id_seq OWNED BY public.product_categories.category_id;


--
-- TOC entry 222 (class 1259 OID 24628)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    seller_id integer NOT NULL,
    category_id integer NOT NULL,
    product_name character varying(64) NOT NULL,
    description character varying(256),
    price numeric(10,2) NOT NULL,
    total_quantity integer DEFAULT 0 NOT NULL,
    date_of_update date DEFAULT CURRENT_DATE
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24627)
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_product_id_seq OWNER TO postgres;

--
-- TOC entry 4916 (class 0 OID 0)
-- Dependencies: 221
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- TOC entry 218 (class 1259 OID 24608)
-- Name: purchase_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.purchase_history (
    purchase_id integer NOT NULL,
    client_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    purchase_date date DEFAULT CURRENT_DATE,
    total_price numeric(10,2) NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.purchase_history OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24607)
-- Name: purchase_history_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.purchase_history_purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purchase_history_purchase_id_seq OWNER TO postgres;

--
-- TOC entry 4917 (class 0 OID 0)
-- Dependencies: 217
-- Name: purchase_history_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.purchase_history_purchase_id_seq OWNED BY public.purchase_history.purchase_id;


--
-- TOC entry 226 (class 1259 OID 24671)
-- Name: supply_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supply_history (
    supply_id integer NOT NULL,
    seller_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    supply_date date DEFAULT CURRENT_DATE
);


ALTER TABLE public.supply_history OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24670)
-- Name: supply_history_supply_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.supply_history_supply_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.supply_history_supply_id_seq OWNER TO postgres;

--
-- TOC entry 4918 (class 0 OID 0)
-- Dependencies: 225
-- Name: supply_history_supply_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.supply_history_supply_id_seq OWNED BY public.supply_history.supply_id;


--
-- TOC entry 220 (class 1259 OID 24615)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(32) NOT NULL,
    password character varying(32) NOT NULL,
    user_role character varying(6) NOT NULL,
    created_at date DEFAULT CURRENT_DATE,
    CONSTRAINT users_password_check CHECK ((length((password)::text) >= 8)),
    CONSTRAINT users_role_check CHECK (((user_role)::text = ANY ((ARRAY['client'::character varying, 'seller'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24614)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 4726 (class 2604 OID 24644)
-- Name: product_categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories ALTER COLUMN category_id SET DEFAULT nextval('public.product_categories_category_id_seq'::regclass);


--
-- TOC entry 4723 (class 2604 OID 24631)
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- TOC entry 4719 (class 2604 OID 24611)
-- Name: purchase_history purchase_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_history ALTER COLUMN purchase_id SET DEFAULT nextval('public.purchase_history_purchase_id_seq'::regclass);


--
-- TOC entry 4727 (class 2604 OID 24674)
-- Name: supply_history supply_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supply_history ALTER COLUMN supply_id SET DEFAULT nextval('public.supply_history_supply_id_seq'::regclass);


--
-- TOC entry 4721 (class 2604 OID 24618)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 4907 (class 0 OID 24641)
-- Dependencies: 224
-- Data for Name: product_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_categories (category_id, category_name, seller_id) FROM stdin;
1	Snacks	1
2	Drinks	1
5	Games	\N
\.


--
-- TOC entry 4905 (class 0 OID 24628)
-- Dependencies: 222
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (product_id, seller_id, category_id, product_name, description, price, total_quantity, date_of_update) FROM stdin;
1	1	1	Cheatos	Cheese corn	101.11	1257	2025-03-18
3	1	2	Cherry juice	Juice	15.00	400	2025-03-18
\.


--
-- TOC entry 4901 (class 0 OID 24608)
-- Dependencies: 218
-- Data for Name: purchase_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.purchase_history (purchase_id, client_id, product_id, quantity, purchase_date, total_price, price) FROM stdin;
1	2	1	10	2025-03-16	1058.90	105.89
2	3	1	20	2025-03-16	2117.80	105.89
3	2	1	200	2025-03-16	21178.00	105.89
4	2	1	70	2025-03-18	10500.00	150.00
5	2	1	30	2025-03-18	4500.00	150.00
6	2	1	1	2025-03-18	150.00	150.00
7	7	1	19	2025-03-18	2850.00	150.00
8	7	1	20	2025-03-18	3000.00	150.00
9	7	1	1	2025-03-18	150.00	150.00
10	7	1	1	2025-03-18	150.00	150.00
11	7	1	1	2025-03-18	150.00	150.00
12	2	3	100	2025-03-19	1500.00	15.00
\.


--
-- TOC entry 4909 (class 0 OID 24671)
-- Dependencies: 226
-- Data for Name: supply_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.supply_history (supply_id, seller_id, product_id, quantity, supply_date) FROM stdin;
1	1	1	50	2025-03-16
2	1	1	150	2025-03-16
3	1	1	500	2025-03-18
4	1	3	250	2025-03-18
\.


--
-- TOC entry 4903 (class 0 OID 24615)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, password, user_role, created_at) FROM stdin;
1	Alim	qwertyui	seller	2025-03-16
2	Ivan	12345678	client	2025-03-16
3	Denis	1q2w3e4r	client	2025-03-16
4	admin	admin123	seller	2025-03-18
5	John	qwertyui	seller	2025-03-18
7	Client	12345678	client	2025-03-18
8	Add	12345678	client	2025-03-19
\.


--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 223
-- Name: product_categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_categories_category_id_seq', 5, true);


--
-- TOC entry 4921 (class 0 OID 0)
-- Dependencies: 221
-- Name: products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_product_id_seq', 3, true);


--
-- TOC entry 4922 (class 0 OID 0)
-- Dependencies: 217
-- Name: purchase_history_purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.purchase_history_purchase_id_seq', 12, true);


--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 225
-- Name: supply_history_supply_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.supply_history_supply_id_seq', 4, true);


--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 8, true);


--
-- TOC entry 4740 (class 2606 OID 24648)
-- Name: product_categories product_categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_category_name_key UNIQUE (category_name);


--
-- TOC entry 4742 (class 2606 OID 24646)
-- Name: product_categories product_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_pkey PRIMARY KEY (category_id);


--
-- TOC entry 4738 (class 2606 OID 24634)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- TOC entry 4732 (class 2606 OID 24613)
-- Name: purchase_history purchase_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_history
    ADD CONSTRAINT purchase_history_pkey PRIMARY KEY (purchase_id);


--
-- TOC entry 4744 (class 2606 OID 24676)
-- Name: supply_history supply_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supply_history
    ADD CONSTRAINT supply_history_pkey PRIMARY KEY (supply_id);


--
-- TOC entry 4734 (class 2606 OID 24622)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4736 (class 2606 OID 24624)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4752 (class 2620 OID 24714)
-- Name: purchase_history calculate; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER calculate BEFORE INSERT ON public.purchase_history FOR EACH ROW EXECUTE FUNCTION public.calculate_total_price();


--
-- TOC entry 4753 (class 2620 OID 24733)
-- Name: product_categories check_category_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER check_category_trigger BEFORE INSERT ON public.product_categories FOR EACH ROW EXECUTE FUNCTION public.check_add_categories();


--
-- TOC entry 4754 (class 2620 OID 24719)
-- Name: supply_history supply_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER supply_trigger AFTER INSERT ON public.supply_history FOR EACH ROW EXECUTE FUNCTION public.update_quantity_on_supply();


--
-- TOC entry 4749 (class 2606 OID 24734)
-- Name: product_categories product_categories_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 4747 (class 2606 OID 24665)
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.product_categories(category_id) ON DELETE RESTRICT;


--
-- TOC entry 4748 (class 2606 OID 24677)
-- Name: products products_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 4745 (class 2606 OID 24697)
-- Name: purchase_history purchase_history_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_history
    ADD CONSTRAINT purchase_history_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 4746 (class 2606 OID 24692)
-- Name: purchase_history purchase_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_history
    ADD CONSTRAINT purchase_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;


--
-- TOC entry 4750 (class 2606 OID 24682)
-- Name: supply_history supply_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supply_history
    ADD CONSTRAINT supply_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;


--
-- TOC entry 4751 (class 2606 OID 24687)
-- Name: supply_history supply_history_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supply_history
    ADD CONSTRAINT supply_history_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


-- Completed on 2025-03-19 17:23:42

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-03-19 17:23:42

--
-- PostgreSQL database cluster dump complete
--

