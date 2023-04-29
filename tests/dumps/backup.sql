SET statement_timeout = 0
SET lock_timeout = 0
SET idle_in_transaction_session_timeout = 0
SET client_encoding = 'UTF8'
SET standard_conforming_strings = on
SELECT pg_catalog.set_config('search_path', '', false)
SET check_function_bodies = false
SET xmloption = content
SET client_min_messages = warning
SET row_security = off
CREATE TYPE public.languageenum AS ENUM ( 'RU', 'EN' )
ALTER TYPE public.languageenum OWNER TO test
CREATE TYPE public.scoreoperationenum AS ENUM ( 'PLUS', 'MINUS' )
ALTER TYPE public.scoreoperationenum OWNER TO test
CREATE TYPE public.variabletypeenum AS ENUM ( 'STR', 'INT', 'BOOL' )
ALTER TYPE public.variabletypeenum OWNER TO test
SET default_tablespace = ''
SET default_table_access_method = heap
CREATE TABLE public.achievement ( id integer NOT NULL, category_id integer NOT NULL, total integer NOT NULL )
ALTER TABLE public.achievement OWNER TO test
CREATE TABLE public.achievement_category ( id integer NOT NULL )
ALTER TABLE public.achievement_category OWNER TO test
CREATE SEQUENCE public.achievement_category_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_category_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_category_id_seq OWNED BY public.achievement_category.id
CREATE TABLE public.achievement_category_translate ( id integer NOT NULL, name character varying NOT NULL, category_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.achievement_category_translate OWNER TO test
CREATE SEQUENCE public.achievement_category_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_category_translate_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_category_translate_id_seq OWNED BY public.achievement_category_translate.id
CREATE SEQUENCE public.achievement_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_id_seq OWNED BY public.achievement.id
CREATE TABLE public.achievement_progress ( id integer NOT NULL, achievement_id integer NOT NULL, entity_name character varying NOT NULL, entity_pointer character varying NOT NULL, counter integer NOT NULL, active boolean NOT NULL, status_id integer NOT NULL )
ALTER TABLE public.achievement_progress OWNER TO test
CREATE SEQUENCE public.achievement_progress_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_progress_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_progress_id_seq OWNED BY public.achievement_progress.id
CREATE TABLE public.achievement_progress_status ( id integer NOT NULL )
ALTER TABLE public.achievement_progress_status OWNER TO test
CREATE SEQUENCE public.achievement_progress_status_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_progress_status_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_progress_status_id_seq OWNED BY public.achievement_progress_status.id
CREATE TABLE public.achievement_progress_status_translate ( id integer NOT NULL, name character varying NOT NULL, status_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.achievement_progress_status_translate OWNER TO test
CREATE SEQUENCE public.achievement_progress_status_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_progress_status_translate_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_progress_status_translate_id_seq OWNED BY public.achievement_progress_status_translate.id
CREATE TABLE public.achievement_translate ( id integer NOT NULL, name character varying NOT NULL, description character varying NOT NULL, achievement_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.achievement_translate OWNER TO test
CREATE SEQUENCE public.achievement_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.achievement_translate_id_seq OWNER TO test
ALTER SEQUENCE public.achievement_translate_id_seq OWNED BY public.achievement_translate.id
CREATE TABLE public.alembic_version ( version_num character varying(32) NOT NULL )
ALTER TABLE public.alembic_version OWNER TO test
CREATE TABLE public.community ( name character varying NOT NULL, description character varying NOT NULL, active boolean NOT NULL, privacy_type_id integer NOT NULL )
ALTER TABLE public.community OWNER TO test
CREATE TABLE public.community_invite ( id integer NOT NULL, community character varying NOT NULL, code character varying NOT NULL, expire_time timestamp without time zone NOT NULL )
ALTER TABLE public.community_invite OWNER TO test
CREATE SEQUENCE public.community_invite_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.community_invite_id_seq OWNER TO test
ALTER SEQUENCE public.community_invite_id_seq OWNED BY public.community_invite.id
CREATE TABLE public.community_mission ( id integer NOT NULL, meeting_date timestamp without time zone NOT NULL, people_required integer, people_max integer, place character varying, comment character varying, community character varying NOT NULL, mission_id integer NOT NULL, status_id integer NOT NULL )
ALTER TABLE public.community_mission OWNER TO test
CREATE SEQUENCE public.community_mission_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.community_mission_id_seq OWNER TO test
ALTER SEQUENCE public.community_mission_id_seq OWNED BY public.community_mission.id
CREATE TABLE public.community_role ( id integer NOT NULL )
ALTER TABLE public.community_role OWNER TO test
CREATE SEQUENCE public.community_role_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.community_role_id_seq OWNER TO test
ALTER SEQUENCE public.community_role_id_seq OWNED BY public.community_role.id
CREATE TABLE public.community_role_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.community_role_translate OWNER TO test
CREATE SEQUENCE public.community_role_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.community_role_translate_id_seq OWNER TO test
ALTER SEQUENCE public.community_role_translate_id_seq OWNED BY public.community_role_translate.id
CREATE TABLE public.community_score ( id integer NOT NULL, community character varying NOT NULL, operation public.scoreoperationenum NOT NULL, value integer NOT NULL )
ALTER TABLE public.community_score OWNER TO test
CREATE SEQUENCE public.community_score_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.community_score_id_seq OWNER TO test
ALTER SEQUENCE public.community_score_id_seq OWNED BY public.community_score.id
CREATE TABLE public."constraint" ( id integer NOT NULL, name character varying NOT NULL, value character varying NOT NULL, value_type public.variabletypeenum NOT NULL )
ALTER TABLE public."constraint" OWNER TO test
CREATE SEQUENCE public.constraint_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.constraint_id_seq OWNER TO test
ALTER SEQUENCE public.constraint_id_seq OWNED BY public."constraint".id
CREATE TABLE public.contact ( id integer NOT NULL, value character varying NOT NULL, type_id integer NOT NULL )
ALTER TABLE public.contact OWNER TO test
CREATE SEQUENCE public.contact_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.contact_id_seq OWNER TO test
ALTER SEQUENCE public.contact_id_seq OWNED BY public.contact.id
CREATE TABLE public.contact_type ( id integer NOT NULL, name character varying NOT NULL )
ALTER TABLE public.contact_type OWNER TO test
CREATE SEQUENCE public.contact_type_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.contact_type_id_seq OWNER TO test
ALTER SEQUENCE public.contact_type_id_seq OWNED BY public.contact_type.id
CREATE TABLE public.contact_type_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.contact_type_translate OWNER TO test
CREATE SEQUENCE public.contact_type_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.contact_type_translate_id_seq OWNER TO test
ALTER SEQUENCE public.contact_type_translate_id_seq OWNED BY public.contact_type_translate.id
CREATE TABLE public.mission ( id integer NOT NULL, active boolean NOT NULL, author character varying NOT NULL, score integer NOT NULL, occupancy_id integer NOT NULL )
ALTER TABLE public.mission OWNER TO test
CREATE SEQUENCE public.mission_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.mission_id_seq OWNER TO test
ALTER SEQUENCE public.mission_id_seq OWNED BY public.mission.id
CREATE TABLE public.mission_translate ( id integer NOT NULL, name character varying NOT NULL, description character varying NOT NULL, instruction character varying NOT NULL, mission_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.mission_translate OWNER TO test
CREATE SEQUENCE public.mission_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.mission_translate_id_seq OWNER TO test
ALTER SEQUENCE public.mission_translate_id_seq OWNED BY public.mission_translate.id
CREATE TABLE public.occupancy_status ( id integer NOT NULL )
ALTER TABLE public.occupancy_status OWNER TO test
CREATE SEQUENCE public.occupancy_status_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.occupancy_status_id_seq OWNER TO test
ALTER SEQUENCE public.occupancy_status_id_seq OWNED BY public.occupancy_status.id
CREATE TABLE public.occupancy_status_translate ( id integer NOT NULL, name character varying NOT NULL, status_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.occupancy_status_translate OWNER TO test
CREATE SEQUENCE public.occupancy_status_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.occupancy_status_translate_id_seq OWNER TO test
ALTER SEQUENCE public.occupancy_status_translate_id_seq OWNED BY public.occupancy_status_translate.id
CREATE TABLE public.occupancy_type ( id integer NOT NULL )
ALTER TABLE public.occupancy_type OWNER TO test
CREATE SEQUENCE public.occupancy_type_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.occupancy_type_id_seq OWNER TO test
ALTER SEQUENCE public.occupancy_type_id_seq OWNED BY public.occupancy_type.id
CREATE TABLE public.occupancy_type_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.occupancy_type_translate OWNER TO test
CREATE SEQUENCE public.occupancy_type_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.occupancy_type_translate_id_seq OWNER TO test
ALTER SEQUENCE public.occupancy_type_translate_id_seq OWNED BY public.occupancy_type_translate.id
CREATE TABLE public.privacy_type ( id integer NOT NULL )
ALTER TABLE public.privacy_type OWNER TO test
CREATE SEQUENCE public.privacy_type_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.privacy_type_id_seq OWNER TO test
ALTER SEQUENCE public.privacy_type_id_seq OWNED BY public.privacy_type.id
CREATE TABLE public.privacy_type_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.privacy_type_translate OWNER TO test
CREATE SEQUENCE public.privacy_type_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.privacy_type_translate_id_seq OWNER TO test
ALTER SEQUENCE public.privacy_type_translate_id_seq OWNED BY public.privacy_type_translate.id
CREATE TABLE public.role_application ( role character varying NOT NULL )
ALTER TABLE public.role_application OWNER TO test
CREATE TABLE public.subscription ( id integer NOT NULL, type_id integer NOT NULL, period_id integer NOT NULL )
ALTER TABLE public.subscription OWNER TO test
CREATE SEQUENCE public.subscription_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_id_seq OWNED BY public.subscription.id
CREATE TABLE public.subscription_period ( id integer NOT NULL, value character varying NOT NULL, unit_id integer NOT NULL )
ALTER TABLE public.subscription_period OWNER TO test
CREATE SEQUENCE public.subscription_period_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_period_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_period_id_seq OWNED BY public.subscription_period.id
CREATE TABLE public.subscription_period_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.subscription_period_translate OWNER TO test
CREATE SEQUENCE public.subscription_period_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_period_translate_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_period_translate_id_seq OWNED BY public.subscription_period_translate.id
CREATE TABLE public.subscription_period_unit ( id integer NOT NULL )
ALTER TABLE public.subscription_period_unit OWNER TO test
CREATE SEQUENCE public.subscription_period_unit_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_period_unit_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_period_unit_id_seq OWNED BY public.subscription_period_unit.id
CREATE TABLE public.subscription_period_unit_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.subscription_period_unit_translate OWNER TO test
CREATE SEQUENCE public.subscription_period_unit_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_period_unit_translate_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_period_unit_translate_id_seq OWNED BY public.subscription_period_unit_translate.id
CREATE TABLE public.subscription_translate ( id integer NOT NULL, name character varying NOT NULL, subscription_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.subscription_translate OWNER TO test
CREATE SEQUENCE public.subscription_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_translate_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_translate_id_seq OWNED BY public.subscription_translate.id
CREATE TABLE public.subscription_type ( id integer NOT NULL )
ALTER TABLE public.subscription_type OWNER TO test
CREATE TABLE public.subscription_type_constraint ( id integer NOT NULL, type_id integer NOT NULL, constraint_id integer NOT NULL )
ALTER TABLE public.subscription_type_constraint OWNER TO test
CREATE SEQUENCE public.subscription_type_constraint_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_type_constraint_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_type_constraint_id_seq OWNED BY public.subscription_type_constraint.id
CREATE SEQUENCE public.subscription_type_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_type_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_type_id_seq OWNED BY public.subscription_type.id
CREATE TABLE public.subscription_type_translate ( id integer NOT NULL, name character varying NOT NULL, type_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.subscription_type_translate OWNER TO test
CREATE SEQUENCE public.subscription_type_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.subscription_type_translate_id_seq OWNER TO test
ALTER SEQUENCE public.subscription_type_translate_id_seq OWNED BY public.subscription_type_translate.id
CREATE TABLE public.task ( id integer NOT NULL, score integer NOT NULL, occupancy_id integer NOT NULL )
ALTER TABLE public.task OWNER TO test
CREATE SEQUENCE public.task_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.task_id_seq OWNER TO test
ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id
CREATE TABLE public.task_translate ( id integer NOT NULL, name character varying NOT NULL, description character varying NOT NULL, task_id integer NOT NULL, language public.languageenum NOT NULL )
ALTER TABLE public.task_translate OWNER TO test
CREATE SEQUENCE public.task_translate_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.task_translate_id_seq OWNER TO test
ALTER SEQUENCE public.task_translate_id_seq OWNED BY public.task_translate.id
CREATE TABLE public."user" ( username character varying NOT NULL, password character varying NOT NULL, active boolean NOT NULL )
ALTER TABLE public."user" OWNER TO test
CREATE TABLE public.user_community ( id integer NOT NULL, username character varying NOT NULL, community_name character varying NOT NULL, role_id integer NOT NULL )
ALTER TABLE public.user_community OWNER TO test
CREATE SEQUENCE public.user_community_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_community_id_seq OWNER TO test
ALTER SEQUENCE public.user_community_id_seq OWNED BY public.user_community.id
CREATE TABLE public.user_contact ( id integer NOT NULL, username character varying NOT NULL, contact_id integer NOT NULL, active boolean NOT NULL )
ALTER TABLE public.user_contact OWNER TO test
CREATE SEQUENCE public.user_contact_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_contact_id_seq OWNER TO test
ALTER SEQUENCE public.user_contact_id_seq OWNED BY public.user_contact.id
CREATE TABLE public.user_mission ( id integer NOT NULL, username character varying NOT NULL, mission_id integer NOT NULL, status_id integer NOT NULL )
ALTER TABLE public.user_mission OWNER TO test
CREATE SEQUENCE public.user_mission_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_mission_id_seq OWNER TO test
ALTER SEQUENCE public.user_mission_id_seq OWNED BY public.user_mission.id
CREATE TABLE public.user_role_application ( id integer NOT NULL, username character varying NOT NULL, role character varying NOT NULL )
ALTER TABLE public.user_role_application OWNER TO test
CREATE SEQUENCE public.user_role_application_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_role_application_id_seq OWNER TO test
ALTER SEQUENCE public.user_role_application_id_seq OWNED BY public.user_role_application.id
CREATE TABLE public.user_score ( id integer NOT NULL, username character varying NOT NULL, operation public.scoreoperationenum NOT NULL, value integer NOT NULL )
ALTER TABLE public.user_score OWNER TO test
CREATE SEQUENCE public.user_score_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_score_id_seq OWNER TO test
ALTER SEQUENCE public.user_score_id_seq OWNED BY public.user_score.id
CREATE TABLE public.user_subscription ( id integer NOT NULL, username character varying NOT NULL, subscription_id integer NOT NULL, cancelled boolean NOT NULL, until_date timestamp without time zone NOT NULL )
ALTER TABLE public.user_subscription OWNER TO test
CREATE SEQUENCE public.user_subscription_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_subscription_id_seq OWNER TO test
ALTER SEQUENCE public.user_subscription_id_seq OWNED BY public.user_subscription.id
CREATE TABLE public.user_task ( id integer NOT NULL, username character varying NOT NULL, task_id integer NOT NULL, status_id integer NOT NULL )
ALTER TABLE public.user_task OWNER TO test
CREATE SEQUENCE public.user_task_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
ALTER TABLE public.user_task_id_seq OWNER TO test
ALTER SEQUENCE public.user_task_id_seq OWNED BY public.user_task.id
CREATE TABLE public.value_type ( name character varying NOT NULL )
ALTER TABLE public.value_type OWNER TO test
ALTER TABLE ONLY public.achievement ALTER COLUMN id SET DEFAULT nextval('public.achievement_id_seq'::regclass)
ALTER TABLE ONLY public.achievement_category ALTER COLUMN id SET DEFAULT nextval('public.achievement_category_id_seq'::regclass)
ALTER TABLE ONLY public.achievement_category_translate ALTER COLUMN id SET DEFAULT nextval('public.achievement_category_translate_id_seq'::regclass)
ALTER TABLE ONLY public.achievement_progress ALTER COLUMN id SET DEFAULT nextval('public.achievement_progress_id_seq'::regclass)
ALTER TABLE ONLY public.achievement_progress_status ALTER COLUMN id SET DEFAULT nextval('public.achievement_progress_status_id_seq'::regclass)
ALTER TABLE ONLY public.achievement_progress_status_translate ALTER COLUMN id SET DEFAULT nextval('public.achievement_progress_status_translate_id_seq'::regclass)
ALTER TABLE ONLY public.achievement_translate ALTER COLUMN id SET DEFAULT nextval('public.achievement_translate_id_seq'::regclass)
ALTER TABLE ONLY public.community_invite ALTER COLUMN id SET DEFAULT nextval('public.community_invite_id_seq'::regclass)
ALTER TABLE ONLY public.community_mission ALTER COLUMN id SET DEFAULT nextval('public.community_mission_id_seq'::regclass)
ALTER TABLE ONLY public.community_role ALTER COLUMN id SET DEFAULT nextval('public.community_role_id_seq'::regclass)
ALTER TABLE ONLY public.community_role_translate ALTER COLUMN id SET DEFAULT nextval('public.community_role_translate_id_seq'::regclass)
ALTER TABLE ONLY public.community_score ALTER COLUMN id SET DEFAULT nextval('public.community_score_id_seq'::regclass)
ALTER TABLE ONLY public."constraint" ALTER COLUMN id SET DEFAULT nextval('public.constraint_id_seq'::regclass)
ALTER TABLE ONLY public.contact ALTER COLUMN id SET DEFAULT nextval('public.contact_id_seq'::regclass)
ALTER TABLE ONLY public.contact_type ALTER COLUMN id SET DEFAULT nextval('public.contact_type_id_seq'::regclass)
ALTER TABLE ONLY public.contact_type_translate ALTER COLUMN id SET DEFAULT nextval('public.contact_type_translate_id_seq'::regclass)
ALTER TABLE ONLY public.mission ALTER COLUMN id SET DEFAULT nextval('public.mission_id_seq'::regclass)
ALTER TABLE ONLY public.mission_translate ALTER COLUMN id SET DEFAULT nextval('public.mission_translate_id_seq'::regclass)
ALTER TABLE ONLY public.occupancy_status ALTER COLUMN id SET DEFAULT nextval('public.occupancy_status_id_seq'::regclass)
ALTER TABLE ONLY public.occupancy_status_translate ALTER COLUMN id SET DEFAULT nextval('public.occupancy_status_translate_id_seq'::regclass)
ALTER TABLE ONLY public.occupancy_type ALTER COLUMN id SET DEFAULT nextval('public.occupancy_type_id_seq'::regclass)
ALTER TABLE ONLY public.occupancy_type_translate ALTER COLUMN id SET DEFAULT nextval('public.occupancy_type_translate_id_seq'::regclass)
ALTER TABLE ONLY public.privacy_type ALTER COLUMN id SET DEFAULT nextval('public.privacy_type_id_seq'::regclass)
ALTER TABLE ONLY public.privacy_type_translate ALTER COLUMN id SET DEFAULT nextval('public.privacy_type_translate_id_seq'::regclass)
ALTER TABLE ONLY public.subscription ALTER COLUMN id SET DEFAULT nextval('public.subscription_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_period ALTER COLUMN id SET DEFAULT nextval('public.subscription_period_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_period_translate ALTER COLUMN id SET DEFAULT nextval('public.subscription_period_translate_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_period_unit ALTER COLUMN id SET DEFAULT nextval('public.subscription_period_unit_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_period_unit_translate ALTER COLUMN id SET DEFAULT nextval('public.subscription_period_unit_translate_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_translate ALTER COLUMN id SET DEFAULT nextval('public.subscription_translate_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_type ALTER COLUMN id SET DEFAULT nextval('public.subscription_type_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_type_constraint ALTER COLUMN id SET DEFAULT nextval('public.subscription_type_constraint_id_seq'::regclass)
ALTER TABLE ONLY public.subscription_type_translate ALTER COLUMN id SET DEFAULT nextval('public.subscription_type_translate_id_seq'::regclass)
ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass)
ALTER TABLE ONLY public.task_translate ALTER COLUMN id SET DEFAULT nextval('public.task_translate_id_seq'::regclass)
ALTER TABLE ONLY public.user_community ALTER COLUMN id SET DEFAULT nextval('public.user_community_id_seq'::regclass)
ALTER TABLE ONLY public.user_contact ALTER COLUMN id SET DEFAULT nextval('public.user_contact_id_seq'::regclass)
ALTER TABLE ONLY public.user_mission ALTER COLUMN id SET DEFAULT nextval('public.user_mission_id_seq'::regclass)
ALTER TABLE ONLY public.user_role_application ALTER COLUMN id SET DEFAULT nextval('public.user_role_application_id_seq'::regclass)
ALTER TABLE ONLY public.user_score ALTER COLUMN id SET DEFAULT nextval('public.user_score_id_seq'::regclass)
ALTER TABLE ONLY public.user_subscription ALTER COLUMN id SET DEFAULT nextval('public.user_subscription_id_seq'::regclass)
ALTER TABLE ONLY public.user_task ALTER COLUMN id SET DEFAULT nextval('public.user_task_id_seq'::regclass)
            INSERT INTO public.alembic_version (version_num) VALUES ('0677b5fb696a')
                                                                SELECT pg_catalog.setval('public.achievement_category_id_seq', 1, false)
SELECT pg_catalog.setval('public.achievement_category_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.achievement_id_seq', 1, false)
SELECT pg_catalog.setval('public.achievement_progress_id_seq', 1, false)
SELECT pg_catalog.setval('public.achievement_progress_status_id_seq', 1, false)
SELECT pg_catalog.setval('public.achievement_progress_status_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.achievement_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.community_invite_id_seq', 1, false)
SELECT pg_catalog.setval('public.community_mission_id_seq', 1, false)
SELECT pg_catalog.setval('public.community_role_id_seq', 1, false)
SELECT pg_catalog.setval('public.community_role_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.community_score_id_seq', 1, false)
SELECT pg_catalog.setval('public.constraint_id_seq', 1, false)
SELECT pg_catalog.setval('public.contact_id_seq', 1, false)
SELECT pg_catalog.setval('public.contact_type_id_seq', 1, false)
SELECT pg_catalog.setval('public.contact_type_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.mission_id_seq', 1, false)
SELECT pg_catalog.setval('public.mission_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.occupancy_status_id_seq', 1, false)
SELECT pg_catalog.setval('public.occupancy_status_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.occupancy_type_id_seq', 1, false)
SELECT pg_catalog.setval('public.occupancy_type_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.privacy_type_id_seq', 1, false)
SELECT pg_catalog.setval('public.privacy_type_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_period_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_period_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_period_unit_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_period_unit_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_type_constraint_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_type_id_seq', 1, false)
SELECT pg_catalog.setval('public.subscription_type_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.task_id_seq', 1, false)
SELECT pg_catalog.setval('public.task_translate_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_community_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_contact_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_mission_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_role_application_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_score_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_subscription_id_seq', 1, false)
SELECT pg_catalog.setval('public.user_task_id_seq', 1, false)
ALTER TABLE ONLY public.achievement_category ADD CONSTRAINT achievement_category_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.achievement_category_translate ADD CONSTRAINT achievement_category_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.achievement ADD CONSTRAINT achievement_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.achievement_progress ADD CONSTRAINT achievement_progress_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.achievement_progress_status ADD CONSTRAINT achievement_progress_status_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.achievement_progress_status_translate ADD CONSTRAINT achievement_progress_status_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.achievement_translate ADD CONSTRAINT achievement_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.alembic_version ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
ALTER TABLE ONLY public.community_invite ADD CONSTRAINT community_invite_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.community_mission ADD CONSTRAINT community_mission_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.community ADD CONSTRAINT community_pkey PRIMARY KEY (name)
ALTER TABLE ONLY public.community_role ADD CONSTRAINT community_role_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.community_role_translate ADD CONSTRAINT community_role_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.community_score ADD CONSTRAINT community_score_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public."constraint" ADD CONSTRAINT constraint_name_key UNIQUE (name)
ALTER TABLE ONLY public."constraint" ADD CONSTRAINT constraint_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.contact ADD CONSTRAINT contact_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.contact_type ADD CONSTRAINT contact_type_name_key UNIQUE (name)
ALTER TABLE ONLY public.contact_type ADD CONSTRAINT contact_type_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.contact_type_translate ADD CONSTRAINT contact_type_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.mission ADD CONSTRAINT mission_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.mission_translate ADD CONSTRAINT mission_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.occupancy_status ADD CONSTRAINT occupancy_status_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.occupancy_status_translate ADD CONSTRAINT occupancy_status_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.occupancy_type ADD CONSTRAINT occupancy_type_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.occupancy_type_translate ADD CONSTRAINT occupancy_type_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.privacy_type ADD CONSTRAINT privacy_type_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.privacy_type_translate ADD CONSTRAINT privacy_type_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.role_application ADD CONSTRAINT role_application_pkey PRIMARY KEY (role)
ALTER TABLE ONLY public.subscription_period ADD CONSTRAINT subscription_period_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_period_translate ADD CONSTRAINT subscription_period_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_period_unit ADD CONSTRAINT subscription_period_unit_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_period_unit_translate ADD CONSTRAINT subscription_period_unit_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription ADD CONSTRAINT subscription_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_translate ADD CONSTRAINT subscription_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_type_constraint ADD CONSTRAINT subscription_type_constraint_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_type ADD CONSTRAINT subscription_type_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.subscription_type_translate ADD CONSTRAINT subscription_type_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.task ADD CONSTRAINT task_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.task_translate ADD CONSTRAINT task_translate_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.user_community ADD CONSTRAINT user_community_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.user_contact ADD CONSTRAINT user_contact_contact_id_key UNIQUE (contact_id)
ALTER TABLE ONLY public.user_contact ADD CONSTRAINT user_contact_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.user_mission ADD CONSTRAINT user_mission_pkey PRIMARY KEY (id, username, mission_id)
ALTER TABLE ONLY public."user" ADD CONSTRAINT user_pkey PRIMARY KEY (username)
ALTER TABLE ONLY public.user_role_application ADD CONSTRAINT user_role_application_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.user_score ADD CONSTRAINT user_score_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.user_subscription ADD CONSTRAINT user_subscription_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.user_task ADD CONSTRAINT user_task_pkey PRIMARY KEY (id)
ALTER TABLE ONLY public.value_type ADD CONSTRAINT value_type_pkey PRIMARY KEY (name)
ALTER TABLE ONLY public.achievement ADD CONSTRAINT achievement_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.achievement_category(id)
ALTER TABLE ONLY public.achievement_category_translate ADD CONSTRAINT achievement_category_translate_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.achievement_category(id)
ALTER TABLE ONLY public.achievement_progress ADD CONSTRAINT achievement_progress_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievement(id)
ALTER TABLE ONLY public.achievement_progress ADD CONSTRAINT achievement_progress_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.achievement_progress_status(id)
ALTER TABLE ONLY public.achievement_progress_status_translate ADD CONSTRAINT achievement_progress_status_translate_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.achievement_progress_status(id)
ALTER TABLE ONLY public.achievement_translate ADD CONSTRAINT achievement_translate_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievement(id)
ALTER TABLE ONLY public.community_invite ADD CONSTRAINT community_invite_community_fkey FOREIGN KEY (community) REFERENCES public.community(name)
ALTER TABLE ONLY public.community_mission ADD CONSTRAINT community_mission_community_fkey FOREIGN KEY (community) REFERENCES public.community(name)
ALTER TABLE ONLY public.community_mission ADD CONSTRAINT community_mission_mission_id_fkey FOREIGN KEY (mission_id) REFERENCES public.mission(id)
ALTER TABLE ONLY public.community_mission ADD CONSTRAINT community_mission_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.occupancy_status(id)
ALTER TABLE ONLY public.community ADD CONSTRAINT community_privacy_type_id_fkey FOREIGN KEY (privacy_type_id) REFERENCES public.privacy_type(id)
ALTER TABLE ONLY public.community_role_translate ADD CONSTRAINT community_role_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.community_role(id)
ALTER TABLE ONLY public.community_score ADD CONSTRAINT community_score_community_fkey FOREIGN KEY (community) REFERENCES public.community(name)
ALTER TABLE ONLY public.contact ADD CONSTRAINT contact_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.contact_type(id)
ALTER TABLE ONLY public.contact_type_translate ADD CONSTRAINT contact_type_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.contact_type(id)
ALTER TABLE ONLY public.mission ADD CONSTRAINT mission_occupancy_id_fkey FOREIGN KEY (occupancy_id) REFERENCES public.occupancy_type(id)
ALTER TABLE ONLY public.mission_translate ADD CONSTRAINT mission_translate_mission_id_fkey FOREIGN KEY (mission_id) REFERENCES public.mission(id)
ALTER TABLE ONLY public.occupancy_status_translate ADD CONSTRAINT occupancy_status_translate_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.occupancy_status(id)
ALTER TABLE ONLY public.occupancy_type_translate ADD CONSTRAINT occupancy_type_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.occupancy_type(id)
ALTER TABLE ONLY public.privacy_type_translate ADD CONSTRAINT privacy_type_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.privacy_type(id)
ALTER TABLE ONLY public.subscription ADD CONSTRAINT subscription_period_id_fkey FOREIGN KEY (period_id) REFERENCES public.subscription_period(id)
ALTER TABLE ONLY public.subscription_period_translate ADD CONSTRAINT subscription_period_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.subscription_period(id)
ALTER TABLE ONLY public.subscription_period ADD CONSTRAINT subscription_period_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.subscription_period_unit(id)
ALTER TABLE ONLY public.subscription_period_unit_translate ADD CONSTRAINT subscription_period_unit_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.subscription_period_unit(id)
ALTER TABLE ONLY public.subscription_translate ADD CONSTRAINT subscription_translate_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscription(id)
ALTER TABLE ONLY public.subscription_type_constraint ADD CONSTRAINT subscription_type_constraint_constraint_id_fkey FOREIGN KEY (constraint_id) REFERENCES public."constraint"(id)
ALTER TABLE ONLY public.subscription_type_constraint ADD CONSTRAINT subscription_type_constraint_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.subscription_type(id)
ALTER TABLE ONLY public.subscription ADD CONSTRAINT subscription_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.subscription_type(id)
ALTER TABLE ONLY public.subscription_type_translate ADD CONSTRAINT subscription_type_translate_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.subscription_type(id)
ALTER TABLE ONLY public.task ADD CONSTRAINT task_occupancy_id_fkey FOREIGN KEY (occupancy_id) REFERENCES public.occupancy_type(id)
ALTER TABLE ONLY public.task_translate ADD CONSTRAINT task_translate_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id)
ALTER TABLE ONLY public.user_community ADD CONSTRAINT user_community_community_name_fkey FOREIGN KEY (community_name) REFERENCES public.community(name)
ALTER TABLE ONLY public.user_community ADD CONSTRAINT user_community_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.community_role(id)
ALTER TABLE ONLY public.user_community ADD CONSTRAINT user_community_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
ALTER TABLE ONLY public.user_contact ADD CONSTRAINT user_contact_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contact(id)
ALTER TABLE ONLY public.user_contact ADD CONSTRAINT user_contact_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
ALTER TABLE ONLY public.user_mission ADD CONSTRAINT user_mission_mission_id_fkey FOREIGN KEY (mission_id) REFERENCES public.mission(id)
ALTER TABLE ONLY public.user_mission ADD CONSTRAINT user_mission_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.occupancy_status(id)
ALTER TABLE ONLY public.user_mission ADD CONSTRAINT user_mission_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
ALTER TABLE ONLY public.user_role_application ADD CONSTRAINT user_role_application_role_fkey FOREIGN KEY (role) REFERENCES public.role_application(role)
ALTER TABLE ONLY public.user_role_application ADD CONSTRAINT user_role_application_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
ALTER TABLE ONLY public.user_score ADD CONSTRAINT user_score_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
ALTER TABLE ONLY public.user_subscription ADD CONSTRAINT user_subscription_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscription(id)
ALTER TABLE ONLY public.user_subscription ADD CONSTRAINT user_subscription_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
ALTER TABLE ONLY public.user_task ADD CONSTRAINT user_task_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.occupancy_status(id)
ALTER TABLE ONLY public.user_task ADD CONSTRAINT user_task_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id)
ALTER TABLE ONLY public.user_task ADD CONSTRAINT user_task_username_fkey FOREIGN KEY (username) REFERENCES public."user"(username)
INSERT INTO public.occupancy_type VALUES (1);
INSERT INTO public.occupancy_status VALUES (1);
INSERT INTO public.occupancy_status_translate VALUES (1, 'В ПРОЦЕССЕ', 1, 'RU');
INSERT INTO public.occupancy_status_translate VALUES (2, 'IN PROGRESS', 1, 'EN');
INSERT INTO public.occupancy_type_translate VALUES (1, 'АМОГУС', 1, 'RU');
INSERT INTO public.occupancy_type_translate VALUES (2, 'AMOGUS', 1, 'EN');
INSERT INTO public.task VALUES (1, 1337, 1);
INSERT INTO public.task_translate VALUES (1, 'СУПЕР ТАСК', 'ДАДА', 1, 'RU');
INSERT INTO public.task_translate VALUES (2, 'SUPER TASK', 'YESYES', 1, 'EN');
INSERT INTO public."user" VALUES ('BIBA', 'B@0B@B', true);
INSERT INTO public.user_task VALUES (1, 'BIBA', 1, 1);