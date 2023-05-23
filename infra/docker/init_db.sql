--
-- PostgreSQL database dump
--

-- Dumped from database version 12.11 (Debian 12.11-1.pgdg110+1)
-- Dumped by pg_dump version 12.11

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

--
-- Name: achievementcategoryenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.achievementcategoryenum AS ENUM (
);


--
-- Name: achievementstatusenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.achievementstatusenum AS ENUM (
    'ACTIVE',
    'FINISH'
);


--
-- Name: communityprivacyenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.communityprivacyenum AS ENUM (
    'PUBLIC',
    'PRIVATE'
);


--
-- Name: communityroleenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.communityroleenum AS ENUM (
    'SUPERUSER',
    'ADMIN',
    'USER',
    'BLOCKED'
);


--
-- Name: contacttypeenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.contacttypeenum AS ENUM (
    'PHONE',
    'MAIL'
);


--
-- Name: languageenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.languageenum AS ENUM (
    'RU',
    'EN'
);


--
-- Name: occupancystatusenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.occupancystatusenum AS ENUM (
    'ACTIVE',
    'FINISH',
    'REJECT',
    'OVERDUE'
);


--
-- Name: scoreoperationenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.scoreoperationenum AS ENUM (
    'PLUS',
    'MINUS'
);


--
-- Name: subscriptionperiodunitenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.subscriptionperiodunitenum AS ENUM (
    'DAY',
    'WEEK',
    'MONTH'
);


--
-- Name: subscriptiontypeenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.subscriptiontypeenum AS ENUM (
    'USUAL',
    'PREMIUM'
);


SET default_table_access_method = heap;

--
-- Name: achievement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.achievement (
    id integer NOT NULL,
    category public.achievementcategoryenum NOT NULL,
    total integer NOT NULL
);


--
-- Name: achievement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.achievement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: achievement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.achievement_id_seq OWNED BY public.achievement.id;


--
-- Name: achievement_progress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.achievement_progress (
    id integer NOT NULL,
    achievement_id integer NOT NULL,
    entity_name character varying NOT NULL,
    entity_pointer character varying NOT NULL,
    counter integer NOT NULL,
    active boolean NOT NULL,
    status public.achievementstatusenum NOT NULL
);


--
-- Name: achievement_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.achievement_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: achievement_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.achievement_progress_id_seq OWNED BY public.achievement_progress.id;


--
-- Name: achievement_translate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.achievement_translate (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    achievement_id integer NOT NULL,
    language public.languageenum NOT NULL
);


--
-- Name: achievement_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.achievement_translate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: achievement_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.achievement_translate_id_seq OWNED BY public.achievement_translate.id;


--
-- Name: community_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.community_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: community; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.community (
    id integer DEFAULT nextval('public.community_id_seq'::regclass) NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    active boolean NOT NULL,
    privacy public.communityprivacyenum NOT NULL
);


--
-- Name: community_invite; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.community_invite (
    id integer NOT NULL,
    community_id integer NOT NULL,
    code character varying NOT NULL,
    expire_time timestamp without time zone NOT NULL
);


--
-- Name: community_invite_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.community_invite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: community_invite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.community_invite_id_seq OWNED BY public.community_invite.id;


--
-- Name: community_mission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.community_mission (
    community_id integer NOT NULL,
    mission_id integer NOT NULL,
    author character varying NOT NULL,
    meeting_date timestamp without time zone,
    people_required integer,
    people_max integer,
    place character varying,
    comment character varying,
    date_close timestamp without time zone,
    status public.occupancystatusenum NOT NULL
);


--
-- Name: community_score; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.community_score (
    id integer NOT NULL,
    community_id integer NOT NULL,
    operation public.scoreoperationenum NOT NULL,
    value integer NOT NULL
);


--
-- Name: community_score_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.community_score_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: community_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.community_score_id_seq OWNED BY public.community_score.id;


--
-- Name: contact; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contact (
    id integer NOT NULL,
    value character varying NOT NULL,
    type public.contacttypeenum NOT NULL
);


--
-- Name: contact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.contact_id_seq OWNED BY public.contact.id;


--
-- Name: mission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mission (
    id integer NOT NULL,
    active boolean NOT NULL,
    author character varying NOT NULL,
    score integer NOT NULL,
    category_id integer NOT NULL
);


--
-- Name: mission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mission_id_seq OWNED BY public.mission.id;


--
-- Name: mission_translate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mission_translate (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    instruction character varying NOT NULL,
    mission_id integer NOT NULL,
    language public.languageenum NOT NULL
);


--
-- Name: mission_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mission_translate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mission_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mission_translate_id_seq OWNED BY public.mission_translate.id;


--
-- Name: occupancy_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.occupancy_category (
    id integer NOT NULL
);


--
-- Name: occupancy_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.occupancy_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: occupancy_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.occupancy_category_id_seq OWNED BY public.occupancy_category.id;


--
-- Name: occupancy_category_translate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.occupancy_category_translate (
    id integer NOT NULL,
    name character varying NOT NULL,
    category_id integer NOT NULL,
    language public.languageenum NOT NULL
);


--
-- Name: occupancy_category_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.occupancy_category_translate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: occupancy_category_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.occupancy_category_translate_id_seq OWNED BY public.occupancy_category_translate.id;


--
-- Name: subscription; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscription (
    id integer NOT NULL,
    type public.subscriptiontypeenum NOT NULL,
    period_id integer NOT NULL
);


--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subscription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.subscription_id_seq OWNED BY public.subscription.id;


--
-- Name: subscription_period; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscription_period (
    id integer NOT NULL,
    value character varying NOT NULL,
    unit public.subscriptionperiodunitenum NOT NULL
);


--
-- Name: subscription_period_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subscription_period_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: subscription_period_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.subscription_period_id_seq OWNED BY public.subscription_period.id;


--
-- Name: subscription_translate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscription_translate (
    id integer NOT NULL,
    name character varying NOT NULL,
    subscription_id integer NOT NULL,
    language public.languageenum NOT NULL
);


--
-- Name: subscription_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subscription_translate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: subscription_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.subscription_translate_id_seq OWNED BY public.subscription_translate.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task (
    id integer NOT NULL,
    score integer NOT NULL,
    category_id integer NOT NULL
);


--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: task_translate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_translate (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    task_id integer NOT NULL,
    language public.languageenum NOT NULL
);


--
-- Name: task_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.task_translate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: task_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.task_translate_id_seq OWNED BY public.task_translate.id;


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id integer DEFAULT nextval('public.user_id_seq'::regclass) NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    active boolean NOT NULL
);


--
-- Name: user_community; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_community (
    user_id integer NOT NULL,
    community_id integer NOT NULL,
    role public.communityroleenum NOT NULL
);


--
-- Name: user_contact; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_contact (
    id integer NOT NULL,
    user_id integer NOT NULL,
    contact_id integer NOT NULL,
    active boolean NOT NULL
);


--
-- Name: user_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_contact_id_seq OWNED BY public.user_contact.id;


--
-- Name: user_mission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_mission (
    user_id integer NOT NULL,
    mission_id integer NOT NULL,
    status public.occupancystatusenum NOT NULL,
    date_close timestamp without time zone
);


--
-- Name: user_score; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_score (
    id integer NOT NULL,
    user_id integer NOT NULL,
    operation public.scoreoperationenum NOT NULL,
    value integer NOT NULL
);


--
-- Name: user_score_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_score_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_score_id_seq OWNED BY public.user_score.id;


--
-- Name: user_subscription; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_subscription (
    id integer NOT NULL,
    user_id integer NOT NULL,
    subscription_id integer NOT NULL,
    cancelled boolean NOT NULL,
    until_date timestamp without time zone NOT NULL
);


--
-- Name: user_subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_subscription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_subscription_id_seq OWNED BY public.user_subscription.id;


--
-- Name: user_task; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_task (
    id integer NOT NULL,
    user_id integer NOT NULL,
    task_id integer NOT NULL,
    status public.occupancystatusenum NOT NULL
);


--
-- Name: user_task_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_task_id_seq OWNED BY public.user_task.id;


--
-- Name: achievement id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement ALTER COLUMN id SET DEFAULT nextval('public.achievement_id_seq'::regclass);


--
-- Name: achievement_progress id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement_progress ALTER COLUMN id SET DEFAULT nextval('public.achievement_progress_id_seq'::regclass);


--
-- Name: achievement_translate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement_translate ALTER COLUMN id SET DEFAULT nextval('public.achievement_translate_id_seq'::regclass);


--
-- Name: community_invite id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_invite ALTER COLUMN id SET DEFAULT nextval('public.community_invite_id_seq'::regclass);


--
-- Name: community_score id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_score ALTER COLUMN id SET DEFAULT nextval('public.community_score_id_seq'::regclass);


--
-- Name: contact id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact ALTER COLUMN id SET DEFAULT nextval('public.contact_id_seq'::regclass);


--
-- Name: mission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission ALTER COLUMN id SET DEFAULT nextval('public.mission_id_seq'::regclass);


--
-- Name: mission_translate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission_translate ALTER COLUMN id SET DEFAULT nextval('public.mission_translate_id_seq'::regclass);


--
-- Name: occupancy_category id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.occupancy_category ALTER COLUMN id SET DEFAULT nextval('public.occupancy_category_id_seq'::regclass);


--
-- Name: occupancy_category_translate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.occupancy_category_translate ALTER COLUMN id SET DEFAULT nextval('public.occupancy_category_translate_id_seq'::regclass);


--
-- Name: subscription id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription ALTER COLUMN id SET DEFAULT nextval('public.subscription_id_seq'::regclass);


--
-- Name: subscription_period id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_period ALTER COLUMN id SET DEFAULT nextval('public.subscription_period_id_seq'::regclass);


--
-- Name: subscription_translate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_translate ALTER COLUMN id SET DEFAULT nextval('public.subscription_translate_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: task_translate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_translate ALTER COLUMN id SET DEFAULT nextval('public.task_translate_id_seq'::regclass);


--
-- Name: user_contact id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_contact ALTER COLUMN id SET DEFAULT nextval('public.user_contact_id_seq'::regclass);


--
-- Name: user_score id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_score ALTER COLUMN id SET DEFAULT nextval('public.user_score_id_seq'::regclass);


--
-- Name: user_subscription id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_subscription ALTER COLUMN id SET DEFAULT nextval('public.user_subscription_id_seq'::regclass);


--
-- Name: user_task id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_task ALTER COLUMN id SET DEFAULT nextval('public.user_task_id_seq'::regclass);


--
-- Data for Name: achievement; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: achievement_progress; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: achievement_translate; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: community; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.community (id, name, description, active, privacy) VALUES (1, 'COMMUNITY_PUBLIC_ACTIVE', 'DAS', true, 'PUBLIC');
INSERT INTO public.community (id, name, description, active, privacy) VALUES (2, 'COMMUNITY_PUBLIC_NOT_ACTIVE', 'DAS', true, 'PUBLIC');
INSERT INTO public.community (id, name, description, active, privacy) VALUES (3, 'COMMUNITY_PRIVATE_ACTIVE', 'ASD', true, 'PRIVATE');
INSERT INTO public.community (id, name, description, active, privacy) VALUES (4, 'COMMUNITY_PRIVATE_NOT_ACTIVE', 'ASD', false, 'PRIVATE');


--
-- Data for Name: community_invite; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: community_mission; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: community_score; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: contact; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: mission; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.mission (id, active, author, score, category_id) VALUES (2, false, 'ABOBUS', 777, 1);
INSERT INTO public.mission (id, active, author, score, category_id) VALUES (1, true, 'ABOBUS', 666, 2);


--
-- Data for Name: mission_translate; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.mission_translate (id, name, description, instruction, mission_id, language) VALUES (1, 'Solve tree', '...', '...', 1, 'EN');
INSERT INTO public.mission_translate (id, name, description, instruction, mission_id, language) VALUES (2, 'Посади дерево', '...', '...', 1, 'RU');
INSERT INTO public.mission_translate (id, name, description, instruction, mission_id, language) VALUES (3, 'swim and swim', '...', '...', 2, 'EN');


--
-- Data for Name: occupancy_category; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.occupancy_category (id) VALUES (1);
INSERT INTO public.occupancy_category (id) VALUES (2);


--
-- Data for Name: occupancy_category_translate; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.occupancy_category_translate (id, name, category_id, language) VALUES (1, 'HOME', 1, 'EN');
INSERT INTO public.occupancy_category_translate (id, name, category_id, language) VALUES (2, 'Дом', 1, 'RU');
INSERT INTO public.occupancy_category_translate (id, name, category_id, language) VALUES (3, 'NATURE', 2, 'EN');


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: subscription_period; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: subscription_translate; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task (id, score, category_id) VALUES (1, 100, 1);
INSERT INTO public.task (id, score, category_id) VALUES (2, 150, 2);


--
-- Data for Name: task_translate; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_translate (id, name, description, task_id, language) VALUES (1, 'Handle Amogus', 'Faster as fuck boy', 1, 'EN');
INSERT INTO public.task_translate (id, name, description, task_id, language) VALUES (2, 'Захвати Амогуса', 'Быстро как никогда прежде', 1, 'RU');
INSERT INTO public.task_translate (id, name, description, task_id, language) VALUES (3, 'Shrek', 'Is love', 2, 'EN');


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."user" (id, username, password, active) VALUES (1, 'USER__ACTIVE', 'PSWD', true);
INSERT INTO public."user" (id, username, password, active) VALUES (2, 'USER__NOT_ACTIVE', 'PSWD', false);


--
-- Data for Name: user_community; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: user_contact; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: user_mission; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: user_score; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: user_subscription; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: user_task; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: achievement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.achievement_id_seq', 1, false);


--
-- Name: achievement_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.achievement_progress_id_seq', 1, false);


--
-- Name: achievement_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.achievement_translate_id_seq', 1, false);


--
-- Name: community_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.community_id_seq', 4, true);


--
-- Name: community_invite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.community_invite_id_seq', 1, false);


--
-- Name: community_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.community_score_id_seq', 1, false);


--
-- Name: contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contact_id_seq', 1, false);


--
-- Name: mission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mission_id_seq', 2, true);


--
-- Name: mission_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mission_translate_id_seq', 3, true);


--
-- Name: occupancy_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.occupancy_category_id_seq', 1, false);


--
-- Name: occupancy_category_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.occupancy_category_translate_id_seq', 3, true);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.subscription_id_seq', 1, false);


--
-- Name: subscription_period_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.subscription_period_id_seq', 1, false);


--
-- Name: subscription_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.subscription_translate_id_seq', 1, false);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_id_seq', 2, true);


--
-- Name: task_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_translate_id_seq', 3, true);


--
-- Name: user_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_contact_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


--
-- Name: user_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_score_id_seq', 1, false);


--
-- Name: user_subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_subscription_id_seq', 1, false);


--
-- Name: user_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_task_id_seq', 1, false);


--
-- Name: achievement achievement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement
    ADD CONSTRAINT achievement_pkey PRIMARY KEY (id);


--
-- Name: achievement_progress achievement_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement_progress
    ADD CONSTRAINT achievement_progress_pkey PRIMARY KEY (id);


--
-- Name: achievement_translate achievement_translate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement_translate
    ADD CONSTRAINT achievement_translate_pkey PRIMARY KEY (id);


--
-- Name: community_invite community_invite_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_invite
    ADD CONSTRAINT community_invite_pkey PRIMARY KEY (id);


--
-- Name: community_mission community_mission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_mission
    ADD CONSTRAINT community_mission_pkey PRIMARY KEY (community_id, mission_id);


--
-- Name: community community_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community
    ADD CONSTRAINT community_name_key UNIQUE (name);


--
-- Name: community community_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community
    ADD CONSTRAINT community_pkey PRIMARY KEY (id);


--
-- Name: community_score community_score_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_score
    ADD CONSTRAINT community_score_pkey PRIMARY KEY (id);


--
-- Name: contact contact_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id);


--
-- Name: mission mission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission
    ADD CONSTRAINT mission_pkey PRIMARY KEY (id);


--
-- Name: mission_translate mission_translate_mission_id_language_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission_translate
    ADD CONSTRAINT mission_translate_mission_id_language_key UNIQUE (mission_id, language);


--
-- Name: mission_translate mission_translate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission_translate
    ADD CONSTRAINT mission_translate_pkey PRIMARY KEY (id);


--
-- Name: occupancy_category occupancy_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.occupancy_category
    ADD CONSTRAINT occupancy_category_pkey PRIMARY KEY (id);


--
-- Name: occupancy_category_translate occupancy_category_translate_category_id_language_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.occupancy_category_translate
    ADD CONSTRAINT occupancy_category_translate_category_id_language_key UNIQUE (category_id, language);


--
-- Name: occupancy_category_translate occupancy_category_translate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.occupancy_category_translate
    ADD CONSTRAINT occupancy_category_translate_pkey PRIMARY KEY (id);


--
-- Name: subscription_period subscription_period_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_period
    ADD CONSTRAINT subscription_period_pkey PRIMARY KEY (id);


--
-- Name: subscription subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_pkey PRIMARY KEY (id);


--
-- Name: subscription_translate subscription_translate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_translate
    ADD CONSTRAINT subscription_translate_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: task_translate task_translate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_translate
    ADD CONSTRAINT task_translate_pkey PRIMARY KEY (id);


--
-- Name: user_community user_community_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_community
    ADD CONSTRAINT user_community_pkey PRIMARY KEY (user_id, community_id);


--
-- Name: user_contact user_contact_contact_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_contact
    ADD CONSTRAINT user_contact_contact_id_key UNIQUE (contact_id);


--
-- Name: user_contact user_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_contact
    ADD CONSTRAINT user_contact_pkey PRIMARY KEY (id);


--
-- Name: user_mission user_mission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mission
    ADD CONSTRAINT user_mission_pkey PRIMARY KEY (user_id, mission_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_score user_score_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_score
    ADD CONSTRAINT user_score_pkey PRIMARY KEY (id);


--
-- Name: user_subscription user_subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_subscription
    ADD CONSTRAINT user_subscription_pkey PRIMARY KEY (id);


--
-- Name: user_task user_task_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_task
    ADD CONSTRAINT user_task_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: achievement_progress achievement_progress_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement_progress
    ADD CONSTRAINT achievement_progress_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievement(id);


--
-- Name: achievement_translate achievement_translate_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievement_translate
    ADD CONSTRAINT achievement_translate_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievement(id);


--
-- Name: community_invite community_invite_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_invite
    ADD CONSTRAINT community_invite_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: community_mission community_mission_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_mission
    ADD CONSTRAINT community_mission_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: community_mission community_mission_mission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_mission
    ADD CONSTRAINT community_mission_mission_id_fkey FOREIGN KEY (mission_id) REFERENCES public.mission(id);


--
-- Name: community_score community_score_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.community_score
    ADD CONSTRAINT community_score_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: mission mission_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission
    ADD CONSTRAINT mission_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.occupancy_category(id);


--
-- Name: mission_translate mission_translate_mission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mission_translate
    ADD CONSTRAINT mission_translate_mission_id_fkey FOREIGN KEY (mission_id) REFERENCES public.mission(id);


--
-- Name: occupancy_category_translate occupancy_category_translate_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.occupancy_category_translate
    ADD CONSTRAINT occupancy_category_translate_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.occupancy_category(id);


--
-- Name: subscription subscription_period_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_period_id_fkey FOREIGN KEY (period_id) REFERENCES public.subscription_period(id);


--
-- Name: subscription_translate subscription_translate_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_translate
    ADD CONSTRAINT subscription_translate_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscription(id);


--
-- Name: task task_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.occupancy_category(id);


--
-- Name: task_translate task_translate_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_translate
    ADD CONSTRAINT task_translate_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id);


--
-- Name: user_community user_community_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_community
    ADD CONSTRAINT user_community_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: user_community user_community_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_community
    ADD CONSTRAINT user_community_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_contact user_contact_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_contact
    ADD CONSTRAINT user_contact_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contact(id);


--
-- Name: user_contact user_contact_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_contact
    ADD CONSTRAINT user_contact_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_mission user_mission_mission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mission
    ADD CONSTRAINT user_mission_mission_id_fkey FOREIGN KEY (mission_id) REFERENCES public.mission(id);


--
-- Name: user_mission user_mission_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mission
    ADD CONSTRAINT user_mission_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_score user_score_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_score
    ADD CONSTRAINT user_score_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_subscription user_subscription_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_subscription
    ADD CONSTRAINT user_subscription_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscription(id);


--
-- Name: user_subscription user_subscription_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_subscription
    ADD CONSTRAINT user_subscription_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_task user_task_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_task
    ADD CONSTRAINT user_task_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id);


--
-- Name: user_task user_task_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_task
    ADD CONSTRAINT user_task_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

