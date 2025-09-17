--
-- PostgreSQL database dump
--

-- Dumped from database version 17.6 (Debian 17.6-1.pgdg12+1)
-- Dumped by pg_dump version 17.5 (Homebrew)

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
-- Name: auth; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA auth;


ALTER SCHEMA auth OWNER TO optitab_db_user;

--
-- Name: extensions; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA extensions;


ALTER SCHEMA extensions OWNER TO optitab_db_user;

--
-- Name: graphql; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA graphql;


ALTER SCHEMA graphql OWNER TO optitab_db_user;

--
-- Name: graphql_public; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA graphql_public;


ALTER SCHEMA graphql_public OWNER TO optitab_db_user;

--
-- Name: pgbouncer; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA pgbouncer;


ALTER SCHEMA pgbouncer OWNER TO optitab_db_user;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO optitab_db_user;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: optitab_db_user
--

COMMENT ON SCHEMA public IS '';


--
-- Name: realtime; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA realtime;


ALTER SCHEMA realtime OWNER TO optitab_db_user;

--
-- Name: storage; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA storage;


ALTER SCHEMA storage OWNER TO optitab_db_user;

--
-- Name: vault; Type: SCHEMA; Schema: -; Owner: optitab_db_user
--

CREATE SCHEMA vault;


ALTER SCHEMA vault OWNER TO optitab_db_user;

--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA extensions;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA extensions;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: aal_level; Type: TYPE; Schema: auth; Owner: optitab_db_user
--

CREATE TYPE auth.aal_level AS ENUM (
    'aal1',
    'aal2',
    'aal3'
);


ALTER TYPE auth.aal_level OWNER TO optitab_db_user;

--
-- Name: code_challenge_method; Type: TYPE; Schema: auth; Owner: optitab_db_user
--

CREATE TYPE auth.code_challenge_method AS ENUM (
    's256',
    'plain'
);


ALTER TYPE auth.code_challenge_method OWNER TO optitab_db_user;

--
-- Name: factor_status; Type: TYPE; Schema: auth; Owner: optitab_db_user
--

CREATE TYPE auth.factor_status AS ENUM (
    'unverified',
    'verified'
);


ALTER TYPE auth.factor_status OWNER TO optitab_db_user;

--
-- Name: factor_type; Type: TYPE; Schema: auth; Owner: optitab_db_user
--

CREATE TYPE auth.factor_type AS ENUM (
    'totp',
    'webauthn',
    'phone'
);


ALTER TYPE auth.factor_type OWNER TO optitab_db_user;

--
-- Name: one_time_token_type; Type: TYPE; Schema: auth; Owner: optitab_db_user
--

CREATE TYPE auth.one_time_token_type AS ENUM (
    'confirmation_token',
    'reauthentication_token',
    'recovery_token',
    'email_change_token_new',
    'email_change_token_current',
    'phone_change_token'
);


ALTER TYPE auth.one_time_token_type OWNER TO optitab_db_user;

--
-- Name: action; Type: TYPE; Schema: realtime; Owner: optitab_db_user
--

CREATE TYPE realtime.action AS ENUM (
    'INSERT',
    'UPDATE',
    'DELETE',
    'TRUNCATE',
    'ERROR'
);


ALTER TYPE realtime.action OWNER TO optitab_db_user;

--
-- Name: equality_op; Type: TYPE; Schema: realtime; Owner: optitab_db_user
--

CREATE TYPE realtime.equality_op AS ENUM (
    'eq',
    'neq',
    'lt',
    'lte',
    'gt',
    'gte',
    'in'
);


ALTER TYPE realtime.equality_op OWNER TO optitab_db_user;

--
-- Name: user_defined_filter; Type: TYPE; Schema: realtime; Owner: optitab_db_user
--

CREATE TYPE realtime.user_defined_filter AS (
	column_name text,
	op realtime.equality_op,
	value text
);


ALTER TYPE realtime.user_defined_filter OWNER TO optitab_db_user;

--
-- Name: wal_column; Type: TYPE; Schema: realtime; Owner: optitab_db_user
--

CREATE TYPE realtime.wal_column AS (
	name text,
	type_name text,
	type_oid oid,
	value jsonb,
	is_pkey boolean,
	is_selectable boolean
);


ALTER TYPE realtime.wal_column OWNER TO optitab_db_user;

--
-- Name: wal_rls; Type: TYPE; Schema: realtime; Owner: optitab_db_user
--

CREATE TYPE realtime.wal_rls AS (
	wal jsonb,
	is_rls_enabled boolean,
	subscription_ids uuid[],
	errors text[]
);


ALTER TYPE realtime.wal_rls OWNER TO optitab_db_user;

--
-- Name: email(); Type: FUNCTION; Schema: auth; Owner: optitab_db_user
--

CREATE FUNCTION auth.email() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.email', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'email')
  )::text
$$;


ALTER FUNCTION auth.email() OWNER TO optitab_db_user;

--
-- Name: FUNCTION email(); Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON FUNCTION auth.email() IS 'Deprecated. Use auth.jwt() -> ''email'' instead.';


--
-- Name: jwt(); Type: FUNCTION; Schema: auth; Owner: optitab_db_user
--

CREATE FUNCTION auth.jwt() RETURNS jsonb
    LANGUAGE sql STABLE
    AS $$
  select 
    coalesce(
        nullif(current_setting('request.jwt.claim', true), ''),
        nullif(current_setting('request.jwt.claims', true), '')
    )::jsonb
$$;


ALTER FUNCTION auth.jwt() OWNER TO optitab_db_user;

--
-- Name: role(); Type: FUNCTION; Schema: auth; Owner: optitab_db_user
--

CREATE FUNCTION auth.role() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.role', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'role')
  )::text
$$;


ALTER FUNCTION auth.role() OWNER TO optitab_db_user;

--
-- Name: FUNCTION role(); Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON FUNCTION auth.role() IS 'Deprecated. Use auth.jwt() -> ''role'' instead.';


--
-- Name: uid(); Type: FUNCTION; Schema: auth; Owner: optitab_db_user
--

CREATE FUNCTION auth.uid() RETURNS uuid
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')
  )::uuid
$$;


ALTER FUNCTION auth.uid() OWNER TO optitab_db_user;

--
-- Name: FUNCTION uid(); Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON FUNCTION auth.uid() IS 'Deprecated. Use auth.jwt() -> ''sub'' instead.';


--
-- Name: grant_pg_cron_access(); Type: FUNCTION; Schema: extensions; Owner: optitab_db_user
--

CREATE FUNCTION extensions.grant_pg_cron_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF EXISTS (
    SELECT
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_cron'
  )
  THEN
    grant usage on schema cron to postgres with grant option;

    alter default privileges in schema cron grant all on tables to postgres with grant option;
    alter default privileges in schema cron grant all on functions to postgres with grant option;
    alter default privileges in schema cron grant all on sequences to postgres with grant option;

    alter default privileges for user supabase_admin in schema cron grant all
        on sequences to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on tables to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on functions to postgres with grant option;

    grant all privileges on all tables in schema cron to postgres with grant option;
    revoke all on table cron.job from postgres;
    grant select on table cron.job to postgres with grant option;
  END IF;
END;
$$;


ALTER FUNCTION extensions.grant_pg_cron_access() OWNER TO optitab_db_user;

--
-- Name: FUNCTION grant_pg_cron_access(); Type: COMMENT; Schema: extensions; Owner: optitab_db_user
--

COMMENT ON FUNCTION extensions.grant_pg_cron_access() IS 'Grants access to pg_cron';


--
-- Name: grant_pg_graphql_access(); Type: FUNCTION; Schema: extensions; Owner: optitab_db_user
--

CREATE FUNCTION extensions.grant_pg_graphql_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE
    func_is_graphql_resolve bool;
BEGIN
    func_is_graphql_resolve = (
        SELECT n.proname = 'resolve'
        FROM pg_event_trigger_ddl_commands() AS ev
        LEFT JOIN pg_catalog.pg_proc AS n
        ON ev.objid = n.oid
    );

    IF func_is_graphql_resolve
    THEN
        -- Update public wrapper to pass all arguments through to the pg_graphql resolve func
        DROP FUNCTION IF EXISTS graphql_public.graphql;
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language sql
        as $$
            select graphql.resolve(
                query := query,
                variables := coalesce(variables, '{}'),
                "operationName" := "operationName",
                extensions := extensions
            );
        $$;

        -- This hook executes when `graphql.resolve` is created. That is not necessarily the last
        -- function in the extension so we need to grant permissions on existing entities AND
        -- update default permissions to any others that are created after `graphql.resolve`
        grant usage on schema graphql to postgres, anon, authenticated, service_role;
        grant select on all tables in schema graphql to postgres, anon, authenticated, service_role;
        grant execute on all functions in schema graphql to postgres, anon, authenticated, service_role;
        grant all on all sequences in schema graphql to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on tables to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on functions to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on sequences to postgres, anon, authenticated, service_role;

        -- Allow postgres role to allow granting usage on graphql and graphql_public schemas to custom roles
        grant usage on schema graphql_public to postgres with grant option;
        grant usage on schema graphql to postgres with grant option;
    END IF;

END;
$_$;


ALTER FUNCTION extensions.grant_pg_graphql_access() OWNER TO optitab_db_user;

--
-- Name: FUNCTION grant_pg_graphql_access(); Type: COMMENT; Schema: extensions; Owner: optitab_db_user
--

COMMENT ON FUNCTION extensions.grant_pg_graphql_access() IS 'Grants access to pg_graphql';


--
-- Name: grant_pg_net_access(); Type: FUNCTION; Schema: extensions; Owner: optitab_db_user
--

CREATE FUNCTION extensions.grant_pg_net_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_net'
  )
  THEN
    IF NOT EXISTS (
      SELECT 1
      FROM pg_roles
      WHERE rolname = 'supabase_functions_admin'
    )
    THEN
      CREATE USER supabase_functions_admin NOINHERIT CREATEROLE LOGIN NOREPLICATION;
    END IF;

    GRANT USAGE ON SCHEMA net TO supabase_functions_admin, postgres, anon, authenticated, service_role;

    IF EXISTS (
      SELECT FROM pg_extension
      WHERE extname = 'pg_net'
      -- all versions in use on existing projects as of 2025-02-20
      -- version 0.12.0 onwards don't need these applied
      AND extversion IN ('0.2', '0.6', '0.7', '0.7.1', '0.8', '0.10.0', '0.11.0')
    ) THEN
      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;

      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;

      REVOKE ALL ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;
      REVOKE ALL ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;

      GRANT EXECUTE ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
      GRANT EXECUTE ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
    END IF;
  END IF;
END;
$$;


ALTER FUNCTION extensions.grant_pg_net_access() OWNER TO optitab_db_user;

--
-- Name: FUNCTION grant_pg_net_access(); Type: COMMENT; Schema: extensions; Owner: optitab_db_user
--

COMMENT ON FUNCTION extensions.grant_pg_net_access() IS 'Grants access to pg_net';


--
-- Name: pgrst_ddl_watch(); Type: FUNCTION; Schema: extensions; Owner: optitab_db_user
--

CREATE FUNCTION extensions.pgrst_ddl_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN SELECT * FROM pg_event_trigger_ddl_commands()
  LOOP
    IF cmd.command_tag IN (
      'CREATE SCHEMA', 'ALTER SCHEMA'
    , 'CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO', 'ALTER TABLE'
    , 'CREATE FOREIGN TABLE', 'ALTER FOREIGN TABLE'
    , 'CREATE VIEW', 'ALTER VIEW'
    , 'CREATE MATERIALIZED VIEW', 'ALTER MATERIALIZED VIEW'
    , 'CREATE FUNCTION', 'ALTER FUNCTION'
    , 'CREATE TRIGGER'
    , 'CREATE TYPE', 'ALTER TYPE'
    , 'CREATE RULE'
    , 'COMMENT'
    )
    -- don't notify in case of CREATE TEMP table or other objects created on pg_temp
    AND cmd.schema_name is distinct from 'pg_temp'
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


ALTER FUNCTION extensions.pgrst_ddl_watch() OWNER TO optitab_db_user;

--
-- Name: pgrst_drop_watch(); Type: FUNCTION; Schema: extensions; Owner: optitab_db_user
--

CREATE FUNCTION extensions.pgrst_drop_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  obj record;
BEGIN
  FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
  LOOP
    IF obj.object_type IN (
      'schema'
    , 'table'
    , 'foreign table'
    , 'view'
    , 'materialized view'
    , 'function'
    , 'trigger'
    , 'type'
    , 'rule'
    )
    AND obj.is_temporary IS false -- no pg_temp objects
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


ALTER FUNCTION extensions.pgrst_drop_watch() OWNER TO optitab_db_user;

--
-- Name: set_graphql_placeholder(); Type: FUNCTION; Schema: extensions; Owner: optitab_db_user
--

CREATE FUNCTION extensions.set_graphql_placeholder() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $_$
    DECLARE
    graphql_is_dropped bool;
    BEGIN
    graphql_is_dropped = (
        SELECT ev.schema_name = 'graphql_public'
        FROM pg_event_trigger_dropped_objects() AS ev
        WHERE ev.schema_name = 'graphql_public'
    );

    IF graphql_is_dropped
    THEN
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language plpgsql
        as $$
            DECLARE
                server_version float;
            BEGIN
                server_version = (SELECT (SPLIT_PART((select version()), ' ', 2))::float);

                IF server_version >= 14 THEN
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql extension is not enabled.'
                            )
                        )
                    );
                ELSE
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql is only available on projects running Postgres 14 onwards.'
                            )
                        )
                    );
                END IF;
            END;
        $$;
    END IF;

    END;
$_$;


ALTER FUNCTION extensions.set_graphql_placeholder() OWNER TO optitab_db_user;

--
-- Name: FUNCTION set_graphql_placeholder(); Type: COMMENT; Schema: extensions; Owner: optitab_db_user
--

COMMENT ON FUNCTION extensions.set_graphql_placeholder() IS 'Reintroduces placeholder function for graphql_public.graphql';


--
-- Name: get_auth(text); Type: FUNCTION; Schema: pgbouncer; Owner: optitab_db_user
--

CREATE FUNCTION pgbouncer.get_auth(p_usename text) RETURNS TABLE(username text, password text)
    LANGUAGE plpgsql SECURITY DEFINER
    AS $_$
begin
    raise debug 'PgBouncer auth request: %', p_usename;

    return query
    select 
        rolname::text, 
        case when rolvaliduntil < now() 
            then null 
            else rolpassword::text 
        end 
    from pg_authid 
    where rolname=$1 and rolcanlogin;
end;
$_$;


ALTER FUNCTION pgbouncer.get_auth(p_usename text) OWNER TO optitab_db_user;

--
-- Name: apply_rls(jsonb, integer); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer DEFAULT (1024 * 1024)) RETURNS SETOF realtime.wal_rls
    LANGUAGE plpgsql
    AS $$
declare
-- Regclass of the table e.g. public.notes
entity_ regclass = (quote_ident(wal ->> 'schema') || '.' || quote_ident(wal ->> 'table'))::regclass;

-- I, U, D, T: insert, update ...
action realtime.action = (
    case wal ->> 'action'
        when 'I' then 'INSERT'
        when 'U' then 'UPDATE'
        when 'D' then 'DELETE'
        else 'ERROR'
    end
);

-- Is row level security enabled for the table
is_rls_enabled bool = relrowsecurity from pg_class where oid = entity_;

subscriptions realtime.subscription[] = array_agg(subs)
    from
        realtime.subscription subs
    where
        subs.entity = entity_;

-- Subscription vars
roles regrole[] = array_agg(distinct us.claims_role::text)
    from
        unnest(subscriptions) us;

working_role regrole;
claimed_role regrole;
claims jsonb;

subscription_id uuid;
subscription_has_access bool;
visible_to_subscription_ids uuid[] = '{}';

-- structured info for wal's columns
columns realtime.wal_column[];
-- previous identity values for update/delete
old_columns realtime.wal_column[];

error_record_exceeds_max_size boolean = octet_length(wal::text) > max_record_bytes;

-- Primary jsonb output for record
output jsonb;

begin
perform set_config('role', null, true);

columns =
    array_agg(
        (
            x->>'name',
            x->>'type',
            x->>'typeoid',
            realtime.cast(
                (x->'value') #>> '{}',
                coalesce(
                    (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                    (x->>'type')::regtype
                )
            ),
            (pks ->> 'name') is not null,
            true
        )::realtime.wal_column
    )
    from
        jsonb_array_elements(wal -> 'columns') x
        left join jsonb_array_elements(wal -> 'pk') pks
            on (x ->> 'name') = (pks ->> 'name');

old_columns =
    array_agg(
        (
            x->>'name',
            x->>'type',
            x->>'typeoid',
            realtime.cast(
                (x->'value') #>> '{}',
                coalesce(
                    (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                    (x->>'type')::regtype
                )
            ),
            (pks ->> 'name') is not null,
            true
        )::realtime.wal_column
    )
    from
        jsonb_array_elements(wal -> 'identity') x
        left join jsonb_array_elements(wal -> 'pk') pks
            on (x ->> 'name') = (pks ->> 'name');

for working_role in select * from unnest(roles) loop

    -- Update `is_selectable` for columns and old_columns
    columns =
        array_agg(
            (
                c.name,
                c.type_name,
                c.type_oid,
                c.value,
                c.is_pkey,
                pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
            )::realtime.wal_column
        )
        from
            unnest(columns) c;

    old_columns =
            array_agg(
                (
                    c.name,
                    c.type_name,
                    c.type_oid,
                    c.value,
                    c.is_pkey,
                    pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
                )::realtime.wal_column
            )
            from
                unnest(old_columns) c;

    if action <> 'DELETE' and count(1) = 0 from unnest(columns) c where c.is_pkey then
        return next (
            jsonb_build_object(
                'schema', wal ->> 'schema',
                'table', wal ->> 'table',
                'type', action
            ),
            is_rls_enabled,
            -- subscriptions is already filtered by entity
            (select array_agg(s.subscription_id) from unnest(subscriptions) as s where claims_role = working_role),
            array['Error 400: Bad Request, no primary key']
        )::realtime.wal_rls;

    -- The claims role does not have SELECT permission to the primary key of entity
    elsif action <> 'DELETE' and sum(c.is_selectable::int) <> count(1) from unnest(columns) c where c.is_pkey then
        return next (
            jsonb_build_object(
                'schema', wal ->> 'schema',
                'table', wal ->> 'table',
                'type', action
            ),
            is_rls_enabled,
            (select array_agg(s.subscription_id) from unnest(subscriptions) as s where claims_role = working_role),
            array['Error 401: Unauthorized']
        )::realtime.wal_rls;

    else
        output = jsonb_build_object(
            'schema', wal ->> 'schema',
            'table', wal ->> 'table',
            'type', action,
            'commit_timestamp', to_char(
                ((wal ->> 'timestamp')::timestamptz at time zone 'utc'),
                'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'
            ),
            'columns', (
                select
                    jsonb_agg(
                        jsonb_build_object(
                            'name', pa.attname,
                            'type', pt.typname
                        )
                        order by pa.attnum asc
                    )
                from
                    pg_attribute pa
                    join pg_type pt
                        on pa.atttypid = pt.oid
                where
                    attrelid = entity_
                    and attnum > 0
                    and pg_catalog.has_column_privilege(working_role, entity_, pa.attname, 'SELECT')
            )
        )
        -- Add "record" key for insert and update
        || case
            when action in ('INSERT', 'UPDATE') then
                jsonb_build_object(
                    'record',
                    (
                        select
                            jsonb_object_agg(
                                -- if unchanged toast, get column name and value from old record
                                coalesce((c).name, (oc).name),
                                case
                                    when (c).name is null then (oc).value
                                    else (c).value
                                end
                            )
                        from
                            unnest(columns) c
                            full outer join unnest(old_columns) oc
                                on (c).name = (oc).name
                        where
                            coalesce((c).is_selectable, (oc).is_selectable)
                            and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                    )
                )
            else '{}'::jsonb
        end
        -- Add "old_record" key for update and delete
        || case
            when action = 'UPDATE' then
                jsonb_build_object(
                        'old_record',
                        (
                            select jsonb_object_agg((c).name, (c).value)
                            from unnest(old_columns) c
                            where
                                (c).is_selectable
                                and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                        )
                    )
            when action = 'DELETE' then
                jsonb_build_object(
                    'old_record',
                    (
                        select jsonb_object_agg((c).name, (c).value)
                        from unnest(old_columns) c
                        where
                            (c).is_selectable
                            and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                            and ( not is_rls_enabled or (c).is_pkey ) -- if RLS enabled, we can't secure deletes so filter to pkey
                    )
                )
            else '{}'::jsonb
        end;

        -- Create the prepared statement
        if is_rls_enabled and action <> 'DELETE' then
            if (select 1 from pg_prepared_statements where name = 'walrus_rls_stmt' limit 1) > 0 then
                deallocate walrus_rls_stmt;
            end if;
            execute realtime.build_prepared_statement_sql('walrus_rls_stmt', entity_, columns);
        end if;

        visible_to_subscription_ids = '{}';

        for subscription_id, claims in (
                select
                    subs.subscription_id,
                    subs.claims
                from
                    unnest(subscriptions) subs
                where
                    subs.entity = entity_
                    and subs.claims_role = working_role
                    and (
                        realtime.is_visible_through_filters(columns, subs.filters)
                        or (
                          action = 'DELETE'
                          and realtime.is_visible_through_filters(old_columns, subs.filters)
                        )
                    )
        ) loop

            if not is_rls_enabled or action = 'DELETE' then
                visible_to_subscription_ids = visible_to_subscription_ids || subscription_id;
            else
                -- Check if RLS allows the role to see the record
                perform
                    -- Trim leading and trailing quotes from working_role because set_config
                    -- doesn't recognize the role as valid if they are included
                    set_config('role', trim(both '"' from working_role::text), true),
                    set_config('request.jwt.claims', claims::text, true);

                execute 'execute walrus_rls_stmt' into subscription_has_access;

                if subscription_has_access then
                    visible_to_subscription_ids = visible_to_subscription_ids || subscription_id;
                end if;
            end if;
        end loop;

        perform set_config('role', null, true);

        return next (
            output,
            is_rls_enabled,
            visible_to_subscription_ids,
            case
                when error_record_exceeds_max_size then array['Error 413: Payload Too Large']
                else '{}'
            end
        )::realtime.wal_rls;

    end if;
end loop;

perform set_config('role', null, true);
end;
$$;


ALTER FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) OWNER TO optitab_db_user;

--
-- Name: broadcast_changes(text, text, text, text, text, record, record, text); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text DEFAULT 'ROW'::text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    -- Declare a variable to hold the JSONB representation of the row
    row_data jsonb := '{}'::jsonb;
BEGIN
    IF level = 'STATEMENT' THEN
        RAISE EXCEPTION 'function can only be triggered for each row, not for each statement';
    END IF;
    -- Check the operation type and handle accordingly
    IF operation = 'INSERT' OR operation = 'UPDATE' OR operation = 'DELETE' THEN
        row_data := jsonb_build_object('old_record', OLD, 'record', NEW, 'operation', operation, 'table', table_name, 'schema', table_schema);
        PERFORM realtime.send (row_data, event_name, topic_name);
    ELSE
        RAISE EXCEPTION 'Unexpected operation type: %', operation;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to process the row: %', SQLERRM;
END;

$$;


ALTER FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) OWNER TO optitab_db_user;

--
-- Name: build_prepared_statement_sql(text, regclass, realtime.wal_column[]); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) RETURNS text
    LANGUAGE sql
    AS $$
      /*
      Builds a sql string that, if executed, creates a prepared statement to
      tests retrive a row from *entity* by its primary key columns.
      Example
          select realtime.build_prepared_statement_sql('public.notes', '{"id"}'::text[], '{"bigint"}'::text[])
      */
          select
      'prepare ' || prepared_statement_name || ' as
          select
              exists(
                  select
                      1
                  from
                      ' || entity || '
                  where
                      ' || string_agg(quote_ident(pkc.name) || '=' || quote_nullable(pkc.value #>> '{}') , ' and ') || '
              )'
          from
              unnest(columns) pkc
          where
              pkc.is_pkey
          group by
              entity
      $$;


ALTER FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) OWNER TO optitab_db_user;

--
-- Name: cast(text, regtype); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime."cast"(val text, type_ regtype) RETURNS jsonb
    LANGUAGE plpgsql IMMUTABLE
    AS $$
    declare
      res jsonb;
    begin
      execute format('select to_jsonb(%L::'|| type_::text || ')', val)  into res;
      return res;
    end
    $$;


ALTER FUNCTION realtime."cast"(val text, type_ regtype) OWNER TO optitab_db_user;

--
-- Name: check_equality_op(realtime.equality_op, regtype, text, text); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) RETURNS boolean
    LANGUAGE plpgsql IMMUTABLE
    AS $$
      /*
      Casts *val_1* and *val_2* as type *type_* and check the *op* condition for truthiness
      */
      declare
          op_symbol text = (
              case
                  when op = 'eq' then '='
                  when op = 'neq' then '!='
                  when op = 'lt' then '<'
                  when op = 'lte' then '<='
                  when op = 'gt' then '>'
                  when op = 'gte' then '>='
                  when op = 'in' then '= any'
                  else 'UNKNOWN OP'
              end
          );
          res boolean;
      begin
          execute format(
              'select %L::'|| type_::text || ' ' || op_symbol
              || ' ( %L::'
              || (
                  case
                      when op = 'in' then type_::text || '[]'
                      else type_::text end
              )
              || ')', val_1, val_2) into res;
          return res;
      end;
      $$;


ALTER FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) OWNER TO optitab_db_user;

--
-- Name: is_visible_through_filters(realtime.wal_column[], realtime.user_defined_filter[]); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) RETURNS boolean
    LANGUAGE sql IMMUTABLE
    AS $_$
    /*
    Should the record be visible (true) or filtered out (false) after *filters* are applied
    */
        select
            -- Default to allowed when no filters present
            $2 is null -- no filters. this should not happen because subscriptions has a default
            or array_length($2, 1) is null -- array length of an empty array is null
            or bool_and(
                coalesce(
                    realtime.check_equality_op(
                        op:=f.op,
                        type_:=coalesce(
                            col.type_oid::regtype, -- null when wal2json version <= 2.4
                            col.type_name::regtype
                        ),
                        -- cast jsonb to text
                        val_1:=col.value #>> '{}',
                        val_2:=f.value
                    ),
                    false -- if null, filter does not match
                )
            )
        from
            unnest(filters) f
            join unnest(columns) col
                on f.column_name = col.name;
    $_$;


ALTER FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) OWNER TO optitab_db_user;

--
-- Name: quote_wal2json(regclass); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.quote_wal2json(entity regclass) RETURNS text
    LANGUAGE sql IMMUTABLE STRICT
    AS $$
      select
        (
          select string_agg('' || ch,'')
          from unnest(string_to_array(nsp.nspname::text, null)) with ordinality x(ch, idx)
          where
            not (x.idx = 1 and x.ch = '"')
            and not (
              x.idx = array_length(string_to_array(nsp.nspname::text, null), 1)
              and x.ch = '"'
            )
        )
        || '.'
        || (
          select string_agg('' || ch,'')
          from unnest(string_to_array(pc.relname::text, null)) with ordinality x(ch, idx)
          where
            not (x.idx = 1 and x.ch = '"')
            and not (
              x.idx = array_length(string_to_array(nsp.nspname::text, null), 1)
              and x.ch = '"'
            )
          )
      from
        pg_class pc
        join pg_namespace nsp
          on pc.relnamespace = nsp.oid
      where
        pc.oid = entity
    $$;


ALTER FUNCTION realtime.quote_wal2json(entity regclass) OWNER TO optitab_db_user;

--
-- Name: send(jsonb, text, text, boolean); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean DEFAULT true) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  BEGIN
    -- Set the topic configuration
    EXECUTE format('SET LOCAL realtime.topic TO %L', topic);

    -- Attempt to insert the message
    INSERT INTO realtime.messages (payload, event, topic, private, extension)
    VALUES (payload, event, topic, private, 'broadcast');
  EXCEPTION
    WHEN OTHERS THEN
      -- Capture and notify the error
      RAISE WARNING 'ErrorSendingBroadcastMessage: %', SQLERRM;
  END;
END;
$$;


ALTER FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) OWNER TO optitab_db_user;

--
-- Name: subscription_check_filters(); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.subscription_check_filters() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    /*
    Validates that the user defined filters for a subscription:
    - refer to valid columns that the claimed role may access
    - values are coercable to the correct column type
    */
    declare
        col_names text[] = coalesce(
                array_agg(c.column_name order by c.ordinal_position),
                '{}'::text[]
            )
            from
                information_schema.columns c
            where
                format('%I.%I', c.table_schema, c.table_name)::regclass = new.entity
                and pg_catalog.has_column_privilege(
                    (new.claims ->> 'role'),
                    format('%I.%I', c.table_schema, c.table_name)::regclass,
                    c.column_name,
                    'SELECT'
                );
        filter realtime.user_defined_filter;
        col_type regtype;

        in_val jsonb;
    begin
        for filter in select * from unnest(new.filters) loop
            -- Filtered column is valid
            if not filter.column_name = any(col_names) then
                raise exception 'invalid column for filter %', filter.column_name;
            end if;

            -- Type is sanitized and safe for string interpolation
            col_type = (
                select atttypid::regtype
                from pg_catalog.pg_attribute
                where attrelid = new.entity
                      and attname = filter.column_name
            );
            if col_type is null then
                raise exception 'failed to lookup type for column %', filter.column_name;
            end if;

            -- Set maximum number of entries for in filter
            if filter.op = 'in'::realtime.equality_op then
                in_val = realtime.cast(filter.value, (col_type::text || '[]')::regtype);
                if coalesce(jsonb_array_length(in_val), 0) > 100 then
                    raise exception 'too many values for `in` filter. Maximum 100';
                end if;
            else
                -- raises an exception if value is not coercable to type
                perform realtime.cast(filter.value, col_type);
            end if;

        end loop;

        -- Apply consistent order to filters so the unique constraint on
        -- (subscription_id, entity, filters) can't be tricked by a different filter order
        new.filters = coalesce(
            array_agg(f order by f.column_name, f.op, f.value),
            '{}'
        ) from unnest(new.filters) f;

        return new;
    end;
    $$;


ALTER FUNCTION realtime.subscription_check_filters() OWNER TO optitab_db_user;

--
-- Name: to_regrole(text); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.to_regrole(role_name text) RETURNS regrole
    LANGUAGE sql IMMUTABLE
    AS $$ select role_name::regrole $$;


ALTER FUNCTION realtime.to_regrole(role_name text) OWNER TO optitab_db_user;

--
-- Name: topic(); Type: FUNCTION; Schema: realtime; Owner: optitab_db_user
--

CREATE FUNCTION realtime.topic() RETURNS text
    LANGUAGE sql STABLE
    AS $$
select nullif(current_setting('realtime.topic', true), '')::text;
$$;


ALTER FUNCTION realtime.topic() OWNER TO optitab_db_user;

--
-- Name: can_insert_object(text, text, uuid, jsonb); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO "storage"."objects" ("bucket_id", "name", "owner", "metadata") VALUES (bucketid, name, owner, metadata);
  -- hack to rollback the successful insert
  RAISE sqlstate 'PT200' using
  message = 'ROLLBACK',
  detail = 'rollback successful insert';
END
$$;


ALTER FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) OWNER TO optitab_db_user;

--
-- Name: extension(text); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.extension(name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
_filename text;
BEGIN
	select string_to_array(name, '/') into _parts;
	select _parts[array_length(_parts,1)] into _filename;
	-- @todo return the last part instead of 2
	return reverse(split_part(reverse(_filename), '.', 1));
END
$$;


ALTER FUNCTION storage.extension(name text) OWNER TO optitab_db_user;

--
-- Name: filename(text); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.filename(name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
BEGIN
	select string_to_array(name, '/') into _parts;
	return _parts[array_length(_parts,1)];
END
$$;


ALTER FUNCTION storage.filename(name text) OWNER TO optitab_db_user;

--
-- Name: foldername(text); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.foldername(name text) RETURNS text[]
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
BEGIN
	select string_to_array(name, '/') into _parts;
	return _parts[1:array_length(_parts,1)-1];
END
$$;


ALTER FUNCTION storage.foldername(name text) OWNER TO optitab_db_user;

--
-- Name: get_size_by_bucket(); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.get_size_by_bucket() RETURNS TABLE(size bigint, bucket_id text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    return query
        select sum((metadata->>'size')::int) as size, obj.bucket_id
        from "storage".objects as obj
        group by obj.bucket_id;
END
$$;


ALTER FUNCTION storage.get_size_by_bucket() OWNER TO optitab_db_user;

--
-- Name: list_multipart_uploads_with_delimiter(text, text, text, integer, text, text); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, next_key_token text DEFAULT ''::text, next_upload_token text DEFAULT ''::text) RETURNS TABLE(key text, id text, created_at timestamp with time zone)
    LANGUAGE plpgsql
    AS $_$
BEGIN
    RETURN QUERY EXECUTE
        'SELECT DISTINCT ON(key COLLATE "C") * from (
            SELECT
                CASE
                    WHEN position($2 IN substring(key from length($1) + 1)) > 0 THEN
                        substring(key from 1 for length($1) + position($2 IN substring(key from length($1) + 1)))
                    ELSE
                        key
                END AS key, id, created_at
            FROM
                storage.s3_multipart_uploads
            WHERE
                bucket_id = $5 AND
                key ILIKE $1 || ''%'' AND
                CASE
                    WHEN $4 != '''' AND $6 = '''' THEN
                        CASE
                            WHEN position($2 IN substring(key from length($1) + 1)) > 0 THEN
                                substring(key from 1 for length($1) + position($2 IN substring(key from length($1) + 1))) COLLATE "C" > $4
                            ELSE
                                key COLLATE "C" > $4
                            END
                    ELSE
                        true
                END AND
                CASE
                    WHEN $6 != '''' THEN
                        id COLLATE "C" > $6
                    ELSE
                        true
                    END
            ORDER BY
                key COLLATE "C" ASC, created_at ASC) as e order by key COLLATE "C" LIMIT $3'
        USING prefix_param, delimiter_param, max_keys, next_key_token, bucket_id, next_upload_token;
END;
$_$;


ALTER FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer, next_key_token text, next_upload_token text) OWNER TO optitab_db_user;

--
-- Name: list_objects_with_delimiter(text, text, text, integer, text, text); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.list_objects_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, start_after text DEFAULT ''::text, next_token text DEFAULT ''::text) RETURNS TABLE(name text, id uuid, metadata jsonb, updated_at timestamp with time zone)
    LANGUAGE plpgsql
    AS $_$
BEGIN
    RETURN QUERY EXECUTE
        'SELECT DISTINCT ON(name COLLATE "C") * from (
            SELECT
                CASE
                    WHEN position($2 IN substring(name from length($1) + 1)) > 0 THEN
                        substring(name from 1 for length($1) + position($2 IN substring(name from length($1) + 1)))
                    ELSE
                        name
                END AS name, id, metadata, updated_at
            FROM
                storage.objects
            WHERE
                bucket_id = $5 AND
                name ILIKE $1 || ''%'' AND
                CASE
                    WHEN $6 != '''' THEN
                    name COLLATE "C" > $6
                ELSE true END
                AND CASE
                    WHEN $4 != '''' THEN
                        CASE
                            WHEN position($2 IN substring(name from length($1) + 1)) > 0 THEN
                                substring(name from 1 for length($1) + position($2 IN substring(name from length($1) + 1))) COLLATE "C" > $4
                            ELSE
                                name COLLATE "C" > $4
                            END
                    ELSE
                        true
                END
            ORDER BY
                name COLLATE "C" ASC) as e order by name COLLATE "C" LIMIT $3'
        USING prefix_param, delimiter_param, max_keys, next_token, bucket_id, start_after;
END;
$_$;


ALTER FUNCTION storage.list_objects_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer, start_after text, next_token text) OWNER TO optitab_db_user;

--
-- Name: operation(); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.operation() RETURNS text
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    RETURN current_setting('storage.operation', true);
END;
$$;


ALTER FUNCTION storage.operation() OWNER TO optitab_db_user;

--
-- Name: search(text, text, integer, integer, integer, text, text, text); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.search(prefix text, bucketname text, limits integer DEFAULT 100, levels integer DEFAULT 1, offsets integer DEFAULT 0, search text DEFAULT ''::text, sortcolumn text DEFAULT 'name'::text, sortorder text DEFAULT 'asc'::text) RETURNS TABLE(name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $_$
declare
  v_order_by text;
  v_sort_order text;
begin
  case
    when sortcolumn = 'name' then
      v_order_by = 'name';
    when sortcolumn = 'updated_at' then
      v_order_by = 'updated_at';
    when sortcolumn = 'created_at' then
      v_order_by = 'created_at';
    when sortcolumn = 'last_accessed_at' then
      v_order_by = 'last_accessed_at';
    else
      v_order_by = 'name';
  end case;

  case
    when sortorder = 'asc' then
      v_sort_order = 'asc';
    when sortorder = 'desc' then
      v_sort_order = 'desc';
    else
      v_sort_order = 'asc';
  end case;

  v_order_by = v_order_by || ' ' || v_sort_order;

  return query execute
    'with folders as (
       select path_tokens[$1] as folder
       from storage.objects
         where objects.name ilike $2 || $3 || ''%''
           and bucket_id = $4
           and array_length(objects.path_tokens, 1) <> $1
       group by folder
       order by folder ' || v_sort_order || '
     )
     (select folder as "name",
            null as id,
            null as updated_at,
            null as created_at,
            null as last_accessed_at,
            null as metadata from folders)
     union all
     (select path_tokens[$1] as "name",
            id,
            updated_at,
            created_at,
            last_accessed_at,
            metadata
     from storage.objects
     where objects.name ilike $2 || $3 || ''%''
       and bucket_id = $4
       and array_length(objects.path_tokens, 1) = $1
     order by ' || v_order_by || ')
     limit $5
     offset $6' using levels, prefix, search, bucketname, limits, offsets;
end;
$_$;


ALTER FUNCTION storage.search(prefix text, bucketname text, limits integer, levels integer, offsets integer, search text, sortcolumn text, sortorder text) OWNER TO optitab_db_user;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: storage; Owner: optitab_db_user
--

CREATE FUNCTION storage.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW; 
END;
$$;


ALTER FUNCTION storage.update_updated_at_column() OWNER TO optitab_db_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_log_entries; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.audit_log_entries (
    instance_id uuid,
    id uuid NOT NULL,
    payload json,
    created_at timestamp with time zone,
    ip_address character varying(64) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE auth.audit_log_entries OWNER TO optitab_db_user;

--
-- Name: TABLE audit_log_entries; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.audit_log_entries IS 'Auth: Audit trail for user actions.';


--
-- Name: flow_state; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.flow_state (
    id uuid NOT NULL,
    user_id uuid,
    auth_code text NOT NULL,
    code_challenge_method auth.code_challenge_method NOT NULL,
    code_challenge text NOT NULL,
    provider_type text NOT NULL,
    provider_access_token text,
    provider_refresh_token text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    authentication_method text NOT NULL,
    auth_code_issued_at timestamp with time zone
);


ALTER TABLE auth.flow_state OWNER TO optitab_db_user;

--
-- Name: TABLE flow_state; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.flow_state IS 'stores metadata for pkce logins';


--
-- Name: identities; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.identities (
    provider_id text NOT NULL,
    user_id uuid NOT NULL,
    identity_data jsonb NOT NULL,
    provider text NOT NULL,
    last_sign_in_at timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    email text GENERATED ALWAYS AS (lower((identity_data ->> 'email'::text))) STORED,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE auth.identities OWNER TO optitab_db_user;

--
-- Name: TABLE identities; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.identities IS 'Auth: Stores identities associated to a user.';


--
-- Name: COLUMN identities.email; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON COLUMN auth.identities.email IS 'Auth: Email is a generated column that references the optional email property in the identity_data';


--
-- Name: instances; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.instances (
    id uuid NOT NULL,
    uuid uuid,
    raw_base_config text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE auth.instances OWNER TO optitab_db_user;

--
-- Name: TABLE instances; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.instances IS 'Auth: Manages users across multiple sites.';


--
-- Name: mfa_amr_claims; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.mfa_amr_claims (
    session_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    authentication_method text NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE auth.mfa_amr_claims OWNER TO optitab_db_user;

--
-- Name: TABLE mfa_amr_claims; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.mfa_amr_claims IS 'auth: stores authenticator method reference claims for multi factor authentication';


--
-- Name: mfa_challenges; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.mfa_challenges (
    id uuid NOT NULL,
    factor_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    verified_at timestamp with time zone,
    ip_address inet NOT NULL,
    otp_code text,
    web_authn_session_data jsonb
);


ALTER TABLE auth.mfa_challenges OWNER TO optitab_db_user;

--
-- Name: TABLE mfa_challenges; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.mfa_challenges IS 'auth: stores metadata about challenge requests made';


--
-- Name: mfa_factors; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.mfa_factors (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    friendly_name text,
    factor_type auth.factor_type NOT NULL,
    status auth.factor_status NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    secret text,
    phone text,
    last_challenged_at timestamp with time zone,
    web_authn_credential jsonb,
    web_authn_aaguid uuid
);


ALTER TABLE auth.mfa_factors OWNER TO optitab_db_user;

--
-- Name: TABLE mfa_factors; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.mfa_factors IS 'auth: stores metadata about factors';


--
-- Name: one_time_tokens; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.one_time_tokens (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token_type auth.one_time_token_type NOT NULL,
    token_hash text NOT NULL,
    relates_to text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT one_time_tokens_token_hash_check CHECK ((char_length(token_hash) > 0))
);


ALTER TABLE auth.one_time_tokens OWNER TO optitab_db_user;

--
-- Name: refresh_tokens; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.refresh_tokens (
    instance_id uuid,
    id bigint NOT NULL,
    token character varying(255),
    user_id character varying(255),
    revoked boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    parent character varying(255),
    session_id uuid
);


ALTER TABLE auth.refresh_tokens OWNER TO optitab_db_user;

--
-- Name: TABLE refresh_tokens; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.refresh_tokens IS 'Auth: Store of tokens used to refresh JWT tokens once they expire.';


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: auth; Owner: optitab_db_user
--

CREATE SEQUENCE auth.refresh_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE auth.refresh_tokens_id_seq OWNER TO optitab_db_user;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: optitab_db_user
--

ALTER SEQUENCE auth.refresh_tokens_id_seq OWNED BY auth.refresh_tokens.id;


--
-- Name: saml_providers; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.saml_providers (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    entity_id text NOT NULL,
    metadata_xml text NOT NULL,
    metadata_url text,
    attribute_mapping jsonb,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    name_id_format text,
    CONSTRAINT "entity_id not empty" CHECK ((char_length(entity_id) > 0)),
    CONSTRAINT "metadata_url not empty" CHECK (((metadata_url = NULL::text) OR (char_length(metadata_url) > 0))),
    CONSTRAINT "metadata_xml not empty" CHECK ((char_length(metadata_xml) > 0))
);


ALTER TABLE auth.saml_providers OWNER TO optitab_db_user;

--
-- Name: TABLE saml_providers; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.saml_providers IS 'Auth: Manages SAML Identity Provider connections.';


--
-- Name: saml_relay_states; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.saml_relay_states (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    request_id text NOT NULL,
    for_email text,
    redirect_to text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    flow_state_id uuid,
    CONSTRAINT "request_id not empty" CHECK ((char_length(request_id) > 0))
);


ALTER TABLE auth.saml_relay_states OWNER TO optitab_db_user;

--
-- Name: TABLE saml_relay_states; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.saml_relay_states IS 'Auth: Contains SAML Relay State information for each Service Provider initiated login.';


--
-- Name: schema_migrations; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.schema_migrations (
    version character varying(255) NOT NULL
);


ALTER TABLE auth.schema_migrations OWNER TO optitab_db_user;

--
-- Name: TABLE schema_migrations; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.schema_migrations IS 'Auth: Manages updates to the auth system.';


--
-- Name: sessions; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    factor_id uuid,
    aal auth.aal_level,
    not_after timestamp with time zone,
    refreshed_at timestamp without time zone,
    user_agent text,
    ip inet,
    tag text
);


ALTER TABLE auth.sessions OWNER TO optitab_db_user;

--
-- Name: TABLE sessions; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.sessions IS 'Auth: Stores session data associated to a user.';


--
-- Name: COLUMN sessions.not_after; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON COLUMN auth.sessions.not_after IS 'Auth: Not after is a nullable column that contains a timestamp after which the session should be regarded as expired.';


--
-- Name: sso_domains; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.sso_domains (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    domain text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    CONSTRAINT "domain not empty" CHECK ((char_length(domain) > 0))
);


ALTER TABLE auth.sso_domains OWNER TO optitab_db_user;

--
-- Name: TABLE sso_domains; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.sso_domains IS 'Auth: Manages SSO email address domain mapping to an SSO Identity Provider.';


--
-- Name: sso_providers; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.sso_providers (
    id uuid NOT NULL,
    resource_id text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    CONSTRAINT "resource_id not empty" CHECK (((resource_id = NULL::text) OR (char_length(resource_id) > 0)))
);


ALTER TABLE auth.sso_providers OWNER TO optitab_db_user;

--
-- Name: TABLE sso_providers; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.sso_providers IS 'Auth: Manages SSO identity provider information; see saml_providers for SAML.';


--
-- Name: COLUMN sso_providers.resource_id; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON COLUMN auth.sso_providers.resource_id IS 'Auth: Uniquely identifies a SSO provider according to a user-chosen resource ID (case insensitive), useful in infrastructure as code.';


--
-- Name: users; Type: TABLE; Schema: auth; Owner: optitab_db_user
--

CREATE TABLE auth.users (
    instance_id uuid,
    id uuid NOT NULL,
    aud character varying(255),
    role character varying(255),
    email character varying(255),
    encrypted_password character varying(255),
    email_confirmed_at timestamp with time zone,
    invited_at timestamp with time zone,
    confirmation_token character varying(255),
    confirmation_sent_at timestamp with time zone,
    recovery_token character varying(255),
    recovery_sent_at timestamp with time zone,
    email_change_token_new character varying(255),
    email_change character varying(255),
    email_change_sent_at timestamp with time zone,
    last_sign_in_at timestamp with time zone,
    raw_app_meta_data jsonb,
    raw_user_meta_data jsonb,
    is_super_admin boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    phone text DEFAULT NULL::character varying,
    phone_confirmed_at timestamp with time zone,
    phone_change text DEFAULT ''::character varying,
    phone_change_token character varying(255) DEFAULT ''::character varying,
    phone_change_sent_at timestamp with time zone,
    confirmed_at timestamp with time zone GENERATED ALWAYS AS (LEAST(email_confirmed_at, phone_confirmed_at)) STORED,
    email_change_token_current character varying(255) DEFAULT ''::character varying,
    email_change_confirm_status smallint DEFAULT 0,
    banned_until timestamp with time zone,
    reauthentication_token character varying(255) DEFAULT ''::character varying,
    reauthentication_sent_at timestamp with time zone,
    is_sso_user boolean DEFAULT false NOT NULL,
    deleted_at timestamp with time zone,
    is_anonymous boolean DEFAULT false NOT NULL,
    CONSTRAINT users_email_change_confirm_status_check CHECK (((email_change_confirm_status >= 0) AND (email_change_confirm_status <= 2)))
);


ALTER TABLE auth.users OWNER TO optitab_db_user;

--
-- Name: TABLE users; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON TABLE auth.users IS 'Auth: Stores user login data within a secure schema.';


--
-- Name: COLUMN users.is_sso_user; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON COLUMN auth.users.is_sso_user IS 'Auth: Set this column to true when the account comes from SSO. These accounts can have duplicate emails.';


--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.account_emailaddress OWNER TO optitab_db_user;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.account_emailaddress ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.account_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE public.account_emailconfirmation OWNER TO optitab_db_user;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.account_emailconfirmation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.account_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ai_aiconversation; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.ai_aiconversation (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    message text NOT NULL,
    ai_response text NOT NULL,
    tokens_used integer NOT NULL,
    model_used character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    contexte_chapitre_id bigint,
    contexte_matiere_id bigint,
    user_id bigint NOT NULL,
    CONSTRAINT ai_aiconversation_ordre_check CHECK ((ordre >= 0)),
    CONSTRAINT ai_aiconversation_tokens_used_check CHECK ((tokens_used >= 0))
);


ALTER TABLE public.ai_aiconversation OWNER TO optitab_db_user;

--
-- Name: ai_aiconversation_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.ai_aiconversation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.ai_aiconversation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO optitab_db_user;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO optitab_db_user;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO optitab_db_user;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO optitab_db_user;

--
-- Name: cours_cours; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.cours_cours (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    contenu text NOT NULL,
    difficulty character varying(10) NOT NULL,
    video_url character varying(200),
    chapitre_id bigint NOT NULL,
    CONSTRAINT cours_cours_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.cours_cours OWNER TO optitab_db_user;

--
-- Name: cours_cours_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.cours_cours ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cours_cours_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cours_coursimage; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.cours_coursimage (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    image_type character varying(20) NOT NULL,
    "position" integer,
    legende character varying(255),
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    cours_id bigint NOT NULL,
    CONSTRAINT cours_coursimage_position_check CHECK (("position" >= 0))
);


ALTER TABLE public.cours_coursimage OWNER TO optitab_db_user;

--
-- Name: cours_coursimage_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.cours_coursimage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cours_coursimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: curriculum_chapitre; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_chapitre (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    contenu text NOT NULL,
    difficulty character varying(10) NOT NULL,
    notion_id bigint NOT NULL,
    CONSTRAINT exercices_chapitre_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.curriculum_chapitre OWNER TO optitab_db_user;

--
-- Name: curriculum_exercice; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_exercice (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    contenu text NOT NULL,
    difficulty character varying(10) NOT NULL,
    question text NOT NULL,
    reponse_correcte text NOT NULL,
    points integer NOT NULL,
    chapitre_id bigint NOT NULL,
    etapes text,
    CONSTRAINT exercices_exercice_ordre_check CHECK ((ordre >= 0)),
    CONSTRAINT exercices_exercice_points_check CHECK ((points >= 0))
);


ALTER TABLE public.curriculum_exercice OWNER TO optitab_db_user;

--
-- Name: curriculum_exerciceimage; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_exerciceimage (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    image_type character varying(20) NOT NULL,
    "position" integer,
    legende character varying(255),
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    exercice_id bigint NOT NULL,
    CONSTRAINT curriculum_exerciceimage_position_check CHECK (("position" >= 0))
);


ALTER TABLE public.curriculum_exerciceimage OWNER TO optitab_db_user;

--
-- Name: curriculum_exerciceimage_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_exerciceimage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.curriculum_exerciceimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: curriculum_matiere; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_matiere (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    description text,
    couleur character varying(7) NOT NULL,
    svg_icon text,
    CONSTRAINT curriculum_matiere_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.curriculum_matiere OWNER TO optitab_db_user;

--
-- Name: curriculum_matiere_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_matiere ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.curriculum_matiere_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: curriculum_matierecontexte; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_matierecontexte (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    description text,
    couleur character varying(7) NOT NULL,
    svg_icon text,
    matiere_id bigint NOT NULL,
    niveau_id bigint NOT NULL,
    CONSTRAINT curriculum_matierecontexte_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.curriculum_matierecontexte OWNER TO optitab_db_user;

--
-- Name: curriculum_matierecontexte_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_matierecontexte ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.curriculum_matierecontexte_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: curriculum_notion; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_notion (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    description text,
    couleur character varying(7) NOT NULL,
    svg_icon text,
    theme_id bigint NOT NULL,
    CONSTRAINT curriculum_notion_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.curriculum_notion OWNER TO optitab_db_user;

--
-- Name: curriculum_notion_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_notion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.curriculum_notion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: curriculum_theme; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.curriculum_theme (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    description text,
    couleur character varying(7) NOT NULL,
    svg_icon text,
    matiere_id bigint NOT NULL,
    contexte_id bigint,
    CONSTRAINT curriculum_theme_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.curriculum_theme OWNER TO optitab_db_user;

--
-- Name: curriculum_theme_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_theme ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.curriculum_theme_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO optitab_db_user;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO optitab_db_user;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO optitab_db_user;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_rest_passwordreset_resetpasswordtoken; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.django_rest_passwordreset_resetpasswordtoken (
    created_at timestamp with time zone NOT NULL,
    key character varying(64) NOT NULL,
    ip_address inet,
    user_agent character varying(512) NOT NULL,
    user_id bigint NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.django_rest_passwordreset_resetpasswordtoken OWNER TO optitab_db_user;

--
-- Name: django_rest_passwordreset_resetpasswordtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.django_rest_passwordreset_resetpasswordtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_rest_passwordreset_resetpasswordtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO optitab_db_user;

--
-- Name: exercices_chapitre_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_chapitre ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.exercices_chapitre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: exercices_exercice_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.curriculum_exercice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.exercices_exercice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: fiches_fichesynthese; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.fiches_fichesynthese (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    contenu_markdown text NOT NULL,
    notion_id bigint NOT NULL,
    CONSTRAINT fiches_fichesynthese_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.fiches_fichesynthese OWNER TO optitab_db_user;

--
-- Name: fiches_fichesynthese_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.fiches_fichesynthese ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.fiches_fichesynthese_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pays_niveau; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.pays_niveau (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    nom character varying(100) NOT NULL,
    ordre integer NOT NULL,
    couleur character varying(7) NOT NULL,
    pays_id bigint NOT NULL,
    CONSTRAINT pays_niveaupays_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.pays_niveau OWNER TO optitab_db_user;

--
-- Name: pays_niveaupays_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.pays_niveau ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.pays_niveaupays_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pays_pays; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.pays_pays (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    nom character varying(100) NOT NULL,
    ordre integer NOT NULL,
    code_iso character varying(3) NOT NULL,
    drapeau_emoji character varying(10),
    CONSTRAINT pays_pays_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.pays_pays OWNER TO optitab_db_user;

--
-- Name: pays_pays_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.pays_pays ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.pays_pays_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: quiz_quiz; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.quiz_quiz (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    contenu text NOT NULL,
    difficulty character varying(10) NOT NULL,
    questions_data jsonb NOT NULL,
    duree_minutes integer NOT NULL,
    chapitre_id bigint NOT NULL,
    CONSTRAINT quiz_quiz_duree_minutes_check CHECK ((duree_minutes >= 0)),
    CONSTRAINT quiz_quiz_ordre_check CHECK ((ordre >= 0))
);


ALTER TABLE public.quiz_quiz OWNER TO optitab_db_user;

--
-- Name: quiz_quiz_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.quiz_quiz ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.quiz_quiz_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: quiz_quizimage; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.quiz_quizimage (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    image_type character varying(20) NOT NULL,
    "position" integer,
    legende character varying(255),
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    quiz_id bigint NOT NULL,
    CONSTRAINT quiz_quizimage_position_check CHECK (("position" >= 0))
);


ALTER TABLE public.quiz_quizimage OWNER TO optitab_db_user;

--
-- Name: quiz_quizimage_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.quiz_quizimage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.quiz_quizimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(200) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data jsonb NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.socialaccount_socialaccount OWNER TO optitab_db_user;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.socialaccount_socialaccount ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL,
    provider_id character varying(200) NOT NULL,
    settings jsonb NOT NULL
);


ALTER TABLE public.socialaccount_socialapp OWNER TO optitab_db_user;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.socialaccount_socialapp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer
);


ALTER TABLE public.socialaccount_socialtoken OWNER TO optitab_db_user;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.socialaccount_socialtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: suivis_suiviexercice; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.suivis_suiviexercice (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    reponse_donnee text NOT NULL,
    est_correct boolean NOT NULL,
    points_obtenus integer NOT NULL,
    temps_seconde integer NOT NULL,
    exercice_id bigint NOT NULL,
    user_id bigint NOT NULL,
    CONSTRAINT suivis_suiviexercice_points_obtenus_check CHECK ((points_obtenus >= 0)),
    CONSTRAINT suivis_suiviexercice_temps_seconde_check CHECK ((temps_seconde >= 0))
);


ALTER TABLE public.suivis_suiviexercice OWNER TO optitab_db_user;

--
-- Name: suivis_suiviexercice_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.suivis_suiviexercice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.suivis_suiviexercice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: suivis_suiviquiz; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.suivis_suiviquiz (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    score integer NOT NULL,
    total_points integer NOT NULL,
    temps_total_seconde integer NOT NULL,
    quiz_id bigint NOT NULL,
    user_id bigint NOT NULL,
    tentative_numero integer NOT NULL,
    xp_gagne integer NOT NULL,
    CONSTRAINT suivis_suiviquiz_score_check CHECK ((score >= 0)),
    CONSTRAINT suivis_suiviquiz_temps_total_seconde_check CHECK ((temps_total_seconde >= 0)),
    CONSTRAINT suivis_suiviquiz_tentative_numero_check CHECK ((tentative_numero >= 0)),
    CONSTRAINT suivis_suiviquiz_total_points_check CHECK ((total_points >= 0)),
    CONSTRAINT suivis_suiviquiz_xp_gagne_check CHECK ((xp_gagne >= 0))
);


ALTER TABLE public.suivis_suiviquiz OWNER TO optitab_db_user;

--
-- Name: suivis_suiviquiz_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.suivis_suiviquiz ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.suivis_suiviquiz_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: synthesis_synthesissheet; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.synthesis_synthesissheet (
    id bigint NOT NULL,
    est_actif boolean NOT NULL,
    date_creation timestamp with time zone NOT NULL,
    date_modification timestamp with time zone NOT NULL,
    titre character varying(200) NOT NULL,
    ordre integer NOT NULL,
    summary text NOT NULL,
    difficulty character varying(10) NOT NULL,
    key_points jsonb NOT NULL,
    formulas jsonb NOT NULL,
    examples jsonb NOT NULL,
    reading_time_minutes integer NOT NULL,
    notion_id bigint NOT NULL,
    CONSTRAINT synthesis_synthesissheet_ordre_check CHECK ((ordre >= 0)),
    CONSTRAINT synthesis_synthesissheet_reading_time_minutes_check CHECK ((reading_time_minutes >= 0))
);


ALTER TABLE public.synthesis_synthesissheet OWNER TO optitab_db_user;

--
-- Name: synthesis_synthesissheet_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.synthesis_synthesissheet ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.synthesis_synthesissheet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_customuser; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_customuser (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    verification_code character varying(6),
    niveau_pays_id bigint,
    pays_id bigint,
    date_joined timestamp with time zone NOT NULL,
    civilite character varying(10),
    date_naissance date,
    telephone character varying(20),
    xp integer NOT NULL,
    role character varying(20) NOT NULL,
    verification_code_sent_at timestamp with time zone,
    streak integer NOT NULL,
    CONSTRAINT users_customuser_streak_check CHECK ((streak >= 0)),
    CONSTRAINT users_customuser_xp_check CHECK ((xp >= 0))
);


ALTER TABLE public.users_customuser OWNER TO optitab_db_user;

--
-- Name: users_customuser_groups; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_customuser_groups (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_customuser_groups OWNER TO optitab_db_user;

--
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_customuser_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_customuser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_customuser_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_customuser ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_customuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_customuser_user_permissions; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_customuser_user_permissions (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_customuser_user_permissions OWNER TO optitab_db_user;

--
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_customuser_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_customuser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_parentchild; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_parentchild (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    child_id bigint NOT NULL,
    parent_id bigint NOT NULL
);


ALTER TABLE public.users_parentchild OWNER TO optitab_db_user;

--
-- Name: users_parentchild_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_parentchild ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_parentchild_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_userfavoritematiere; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_userfavoritematiere (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    matiere_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.users_userfavoritematiere OWNER TO optitab_db_user;

--
-- Name: users_userfavoritematiere_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_userfavoritematiere ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_userfavoritematiere_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_usernotification; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_usernotification (
    id bigint NOT NULL,
    type character varying(50) NOT NULL,
    title character varying(200),
    message text,
    data jsonb,
    read boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.users_usernotification OWNER TO optitab_db_user;

--
-- Name: users_usernotification_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_usernotification ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_usernotification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_userselectedmatiere; Type: TABLE; Schema: public; Owner: optitab_db_user
--

CREATE TABLE public.users_userselectedmatiere (
    id bigint NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    matiere_id bigint NOT NULL,
    user_id bigint NOT NULL,
    CONSTRAINT users_userselectedmatiere_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.users_userselectedmatiere OWNER TO optitab_db_user;

--
-- Name: users_userselectedmatiere_id_seq; Type: SEQUENCE; Schema: public; Owner: optitab_db_user
--

ALTER TABLE public.users_userselectedmatiere ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_userselectedmatiere_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: messages; Type: TABLE; Schema: realtime; Owner: optitab_db_user
--

CREATE TABLE realtime.messages (
    topic text NOT NULL,
    extension text NOT NULL,
    payload jsonb,
    event text,
    private boolean DEFAULT false,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    inserted_at timestamp without time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
)
PARTITION BY RANGE (inserted_at);


ALTER TABLE realtime.messages OWNER TO optitab_db_user;

--
-- Name: schema_migrations; Type: TABLE; Schema: realtime; Owner: optitab_db_user
--

CREATE TABLE realtime.schema_migrations (
    version bigint NOT NULL,
    inserted_at timestamp(0) without time zone
);


ALTER TABLE realtime.schema_migrations OWNER TO optitab_db_user;

--
-- Name: subscription; Type: TABLE; Schema: realtime; Owner: optitab_db_user
--

CREATE TABLE realtime.subscription (
    id bigint NOT NULL,
    subscription_id uuid NOT NULL,
    entity regclass NOT NULL,
    filters realtime.user_defined_filter[] DEFAULT '{}'::realtime.user_defined_filter[] NOT NULL,
    claims jsonb NOT NULL,
    claims_role regrole GENERATED ALWAYS AS (realtime.to_regrole((claims ->> 'role'::text))) STORED NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE realtime.subscription OWNER TO optitab_db_user;

--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: realtime; Owner: optitab_db_user
--

ALTER TABLE realtime.subscription ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME realtime.subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: buckets; Type: TABLE; Schema: storage; Owner: optitab_db_user
--

CREATE TABLE storage.buckets (
    id text NOT NULL,
    name text NOT NULL,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    public boolean DEFAULT false,
    avif_autodetection boolean DEFAULT false,
    file_size_limit bigint,
    allowed_mime_types text[],
    owner_id text
);


ALTER TABLE storage.buckets OWNER TO optitab_db_user;

--
-- Name: COLUMN buckets.owner; Type: COMMENT; Schema: storage; Owner: optitab_db_user
--

COMMENT ON COLUMN storage.buckets.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: migrations; Type: TABLE; Schema: storage; Owner: optitab_db_user
--

CREATE TABLE storage.migrations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    hash character varying(40) NOT NULL,
    executed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE storage.migrations OWNER TO optitab_db_user;

--
-- Name: objects; Type: TABLE; Schema: storage; Owner: optitab_db_user
--

CREATE TABLE storage.objects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    bucket_id text,
    name text,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    last_accessed_at timestamp with time zone DEFAULT now(),
    metadata jsonb,
    path_tokens text[] GENERATED ALWAYS AS (string_to_array(name, '/'::text)) STORED,
    version text,
    owner_id text,
    user_metadata jsonb
);


ALTER TABLE storage.objects OWNER TO optitab_db_user;

--
-- Name: COLUMN objects.owner; Type: COMMENT; Schema: storage; Owner: optitab_db_user
--

COMMENT ON COLUMN storage.objects.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: s3_multipart_uploads; Type: TABLE; Schema: storage; Owner: optitab_db_user
--

CREATE TABLE storage.s3_multipart_uploads (
    id text NOT NULL,
    in_progress_size bigint DEFAULT 0 NOT NULL,
    upload_signature text NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    version text NOT NULL,
    owner_id text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    user_metadata jsonb
);


ALTER TABLE storage.s3_multipart_uploads OWNER TO optitab_db_user;

--
-- Name: s3_multipart_uploads_parts; Type: TABLE; Schema: storage; Owner: optitab_db_user
--

CREATE TABLE storage.s3_multipart_uploads_parts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    upload_id text NOT NULL,
    size bigint DEFAULT 0 NOT NULL,
    part_number integer NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    etag text NOT NULL,
    owner_id text,
    version text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.s3_multipart_uploads_parts OWNER TO optitab_db_user;

--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('auth.refresh_tokens_id_seq'::regclass);


--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.audit_log_entries (instance_id, id, payload, created_at, ip_address) FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.flow_state (id, user_id, auth_code, code_challenge_method, code_challenge, provider_type, provider_access_token, provider_refresh_token, created_at, updated_at, authentication_method, auth_code_issued_at) FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.identities (provider_id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at, id) FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.instances (id, uuid, raw_base_config, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.mfa_amr_claims (session_id, created_at, updated_at, authentication_method, id) FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.mfa_challenges (id, factor_id, created_at, verified_at, ip_address, otp_code, web_authn_session_data) FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.mfa_factors (id, user_id, friendly_name, factor_type, status, created_at, updated_at, secret, phone, last_challenged_at, web_authn_credential, web_authn_aaguid) FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.one_time_tokens (id, user_id, token_type, token_hash, relates_to, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.refresh_tokens (instance_id, id, token, user_id, revoked, created_at, updated_at, parent, session_id) FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.saml_providers (id, sso_provider_id, entity_id, metadata_xml, metadata_url, attribute_mapping, created_at, updated_at, name_id_format) FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.saml_relay_states (id, sso_provider_id, request_id, for_email, redirect_to, created_at, updated_at, flow_state_id) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.schema_migrations (version) FROM stdin;
20171026211738
20171026211808
20171026211834
20180103212743
20180108183307
20180119214651
20180125194653
00
20210710035447
20210722035447
20210730183235
20210909172000
20210927181326
20211122151130
20211124214934
20211202183645
20220114185221
20220114185340
20220224000811
20220323170000
20220429102000
20220531120530
20220614074223
20220811173540
20221003041349
20221003041400
20221011041400
20221020193600
20221021073300
20221021082433
20221027105023
20221114143122
20221114143410
20221125140132
20221208132122
20221215195500
20221215195800
20221215195900
20230116124310
20230116124412
20230131181311
20230322519590
20230402418590
20230411005111
20230508135423
20230523124323
20230818113222
20230914180801
20231027141322
20231114161723
20231117164230
20240115144230
20240214120130
20240306115329
20240314092811
20240427152123
20240612123726
20240729123726
20240802193726
20240806073726
20241009103726
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.sessions (id, user_id, created_at, updated_at, factor_id, aal, not_after, refreshed_at, user_agent, ip, tag) FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.sso_domains (id, sso_provider_id, domain, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.sso_providers (id, resource_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: optitab_db_user
--

COPY auth.users (instance_id, id, aud, role, email, encrypted_password, email_confirmed_at, invited_at, confirmation_token, confirmation_sent_at, recovery_token, recovery_sent_at, email_change_token_new, email_change, email_change_sent_at, last_sign_in_at, raw_app_meta_data, raw_user_meta_data, is_super_admin, created_at, updated_at, phone, phone_confirmed_at, phone_change, phone_change_token, phone_change_sent_at, email_change_token_current, email_change_confirm_status, banned_until, reauthentication_token, reauthentication_sent_at, is_sso_user, deleted_at, is_anonymous) FROM stdin;
\.


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
\.


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Data for Name: ai_aiconversation; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.ai_aiconversation (id, est_actif, date_creation, date_modification, titre, ordre, message, ai_response, tokens_used, model_used, created_at, contexte_chapitre_id, contexte_matiere_id, user_id) FROM stdin;
1	t	2025-09-06 21:17:52.651301+00	2025-09-06 21:17:52.651313+00		0	c'est quoi une suite arithmétique	Erreur lors de la génération de la réponse: \n\nYou tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.\n\nYou can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. \n\nAlternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`\n\nA detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742\n	0	gpt-3.5-turbo	2025-09-06 21:17:52.65134+00	\N	\N	2
2	t	2025-09-06 21:22:56.335873+00	2025-09-06 21:22:56.335894+00		0	Explique-moi les dérivées	Erreur lors de la génération de la réponse: No module named 'pkg_resources'	0	gpt-3.5-turbo	2025-09-06 21:22:56.335942+00	\N	\N	2
3	t	2025-09-06 21:25:48.325288+00	2025-09-06 21:25:48.325317+00		0	Explique-moi les dérivées	Erreur lors de la génération de la réponse: You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.	0	gpt-3.5-turbo	2025-09-06 21:25:48.325361+00	\N	\N	2
4	t	2025-09-06 21:28:54.220856+00	2025-09-06 21:28:54.220892+00		0	Explique-moi les dérivées	Erreur lors de la génération de la réponse: You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.	0	gpt-3.5-turbo	2025-09-06 21:28:54.220955+00	\N	\N	2
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add custom user	6	add_customuser
22	Can change custom user	6	change_customuser
23	Can delete custom user	6	delete_customuser
24	Can view custom user	6	view_customuser
25	Can add Matière favorite	7	add_userfavoritematiere
26	Can change Matière favorite	7	change_userfavoritematiere
27	Can delete Matière favorite	7	delete_userfavoritematiere
28	Can view Matière favorite	7	view_userfavoritematiere
29	Can add Matière sélectionnée	8	add_userselectedmatiere
30	Can change Matière sélectionnée	8	change_userselectedmatiere
31	Can delete Matière sélectionnée	8	delete_userselectedmatiere
32	Can view Matière sélectionnée	8	view_userselectedmatiere
33	Can add Password Reset Token	9	add_resetpasswordtoken
34	Can change Password Reset Token	9	change_resetpasswordtoken
35	Can delete Password Reset Token	9	delete_resetpasswordtoken
36	Can view Password Reset Token	9	view_resetpasswordtoken
37	Can add Notion	10	add_notion
38	Can change Notion	10	change_notion
39	Can delete Notion	10	delete_notion
40	Can view Notion	10	view_notion
41	Can add Matière	11	add_matiere
42	Can change Matière	11	change_matiere
43	Can delete Matière	11	delete_matiere
44	Can view Matière	11	view_matiere
45	Can add Chapitre	12	add_chapitre
46	Can change Chapitre	12	change_chapitre
47	Can delete Chapitre	12	delete_chapitre
48	Can view Chapitre	12	view_chapitre
49	Can add Thème	13	add_theme
50	Can change Thème	13	change_theme
51	Can delete Thème	13	delete_theme
52	Can view Thème	13	view_theme
53	Can add Exercice	14	add_exercice
54	Can change Exercice	14	change_exercice
55	Can delete Exercice	14	delete_exercice
56	Can view Exercice	14	view_exercice
57	Can add Cours	15	add_cours
58	Can change Cours	15	change_cours
59	Can delete Cours	15	delete_cours
60	Can view Cours	15	view_cours
61	Can add suivi quiz	16	add_suiviquiz
62	Can change suivi quiz	16	change_suiviquiz
63	Can delete suivi quiz	16	delete_suiviquiz
64	Can view suivi quiz	16	view_suiviquiz
65	Can add suivi exercice	17	add_suiviexercice
66	Can change suivi exercice	17	change_suiviexercice
67	Can delete suivi exercice	17	delete_suiviexercice
68	Can view suivi exercice	17	view_suiviexercice
69	Can add Fiche de Synthèse	18	add_fichesynthese
70	Can change Fiche de Synthèse	18	change_fichesynthese
71	Can delete Fiche de Synthèse	18	delete_fichesynthese
72	Can view Fiche de Synthèse	18	view_fichesynthese
73	Can add Quiz	19	add_quiz
74	Can change Quiz	19	change_quiz
75	Can delete Quiz	19	delete_quiz
76	Can view Quiz	19	view_quiz
77	Can add Pays	20	add_pays
78	Can change Pays	20	change_pays
79	Can delete Pays	20	delete_pays
80	Can view Pays	20	view_pays
81	Can add niveau pays	21	add_niveaupays
82	Can change niveau pays	21	change_niveaupays
83	Can delete niveau pays	21	delete_niveaupays
84	Can view niveau pays	21	view_niveaupays
85	Can add Matière	22	add_matiere
86	Can change Matière	22	change_matiere
87	Can delete Matière	22	delete_matiere
88	Can view Matière	22	view_matiere
89	Can add Thème	23	add_theme
90	Can change Thème	23	change_theme
91	Can delete Thème	23	delete_theme
92	Can view Thème	23	view_theme
93	Can add Notion	24	add_notion
94	Can change Notion	24	change_notion
95	Can delete Notion	24	delete_notion
96	Can view Notion	24	view_notion
97	Can add Chapitre	25	add_chapitre
98	Can change Chapitre	25	change_chapitre
99	Can delete Chapitre	25	delete_chapitre
100	Can view Chapitre	25	view_chapitre
101	Can add Exercice	26	add_exercice
102	Can change Exercice	26	change_exercice
103	Can delete Exercice	26	delete_exercice
104	Can view Exercice	26	view_exercice
105	Can add niveau	21	add_niveau
106	Can change niveau	21	change_niveau
107	Can delete niveau	21	delete_niveau
108	Can view niveau	21	view_niveau
109	Can add Contexte Matière	27	add_matierecontexte
110	Can change Contexte Matière	27	change_matierecontexte
111	Can delete Contexte Matière	27	delete_matierecontexte
112	Can view Contexte Matière	27	view_matierecontexte
113	Can add Image d'exercice	28	add_exerciceimage
114	Can change Image d'exercice	28	change_exerciceimage
115	Can delete Image d'exercice	28	delete_exerciceimage
116	Can view Image d'exercice	28	view_exerciceimage
117	Can add Lien parent-enfant	29	add_parentchild
118	Can change Lien parent-enfant	29	change_parentchild
119	Can delete Lien parent-enfant	29	delete_parentchild
120	Can view Lien parent-enfant	29	view_parentchild
121	Can add Fiche de synthèse	30	add_synthesissheet
122	Can change Fiche de synthèse	30	change_synthesissheet
123	Can delete Fiche de synthèse	30	delete_synthesissheet
124	Can view Fiche de synthèse	30	view_synthesissheet
125	Can add Image de quiz	31	add_quizimage
126	Can change Image de quiz	31	change_quizimage
127	Can delete Image de quiz	31	delete_quizimage
128	Can view Image de quiz	31	view_quizimage
129	Can add user notification	32	add_usernotification
130	Can change user notification	32	change_usernotification
131	Can delete user notification	32	delete_usernotification
132	Can view user notification	32	view_usernotification
133	Can add Image de cours	33	add_coursimage
134	Can change Image de cours	33	change_coursimage
135	Can delete Image de cours	33	delete_coursimage
136	Can view Image de cours	33	view_coursimage
137	Can add Token	34	add_token
138	Can change Token	34	change_token
139	Can delete Token	34	delete_token
140	Can view Token	34	view_token
141	Can add Token	35	add_tokenproxy
142	Can change Token	35	change_tokenproxy
143	Can delete Token	35	delete_tokenproxy
144	Can view Token	35	view_tokenproxy
145	Can add email address	36	add_emailaddress
146	Can change email address	36	change_emailaddress
147	Can delete email address	36	delete_emailaddress
148	Can view email address	36	view_emailaddress
149	Can add email confirmation	37	add_emailconfirmation
150	Can change email confirmation	37	change_emailconfirmation
151	Can delete email confirmation	37	delete_emailconfirmation
152	Can view email confirmation	37	view_emailconfirmation
153	Can add social account	38	add_socialaccount
154	Can change social account	38	change_socialaccount
155	Can delete social account	38	delete_socialaccount
156	Can view social account	38	view_socialaccount
157	Can add social application	39	add_socialapp
158	Can change social application	39	change_socialapp
159	Can delete social application	39	delete_socialapp
160	Can view social application	39	view_socialapp
161	Can add social application token	40	add_socialtoken
162	Can change social application token	40	change_socialtoken
163	Can delete social application token	40	delete_socialtoken
164	Can view social application token	40	view_socialtoken
165	Can add Conversation IA	41	add_aiconversation
166	Can change Conversation IA	41	change_aiconversation
167	Can delete Conversation IA	41	delete_aiconversation
168	Can view Conversation IA	41	view_aiconversation
169	Can add Streak quotidien	42	add_userdailystreak
170	Can change Streak quotidien	42	change_userdailystreak
171	Can delete Streak quotidien	42	delete_userdailystreak
172	Can view Streak quotidien	42	view_userdailystreak
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- Data for Name: cours_cours; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.cours_cours (id, est_actif, date_creation, date_modification, titre, ordre, contenu, difficulty, video_url, chapitre_id) FROM stdin;
16	t	2025-09-04 08:49:20.056619+00	2025-09-04 08:49:20.056645+00	Introduction aux limites et intuitions	0	Contenu:\n<div style="background:#f9f9f9; padding:20px; border-radius:12px;">\n<h2 style="color:#2c3e50;">I. Pourquoi étudier les limites ?</h2>\n<p>Une suite $(u_n)$ est une liste de nombres indexés par $n$.\nÉtudier sa limite permet de comprendre son comportement lorsque $n$ devient très grand :</p>\n<ul>\n<li>Elle peut <strong>se stabiliser</strong> vers une valeur.</li>\n<li>Elle peut <strong>croître indéfiniment</strong> ou <strong>décroître indéfiniment</strong>.</li>\n<li>Elle peut <strong>osciller</strong> sans se fixer.</li>\n</ul>\n<h2 style="color:#2980b9;">II. Définitions essentielles</h2>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Définition 1 : Limite finie</strong><br>\nUne suite $(u_n)$ tend vers un réel $L$ si, pour tout $\\varepsilon > 0$, il existe un rang $n_0$ tel que pour tout $n \\ge n_0$ :<br>\n$$|u_n - L| < \\varepsilon.$$<br>\nNotation : $$\\lim_{n\\to\\infty} u_n = L.$$\n</div>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Définition 2 : Limite infinie positive</strong><br>\n$(u_n) \\to +\\infty$ si pour tout réel $A$, il existe $n_0$ tel que pour $n \\ge n_0$, $u_n > A$.<br>\nNotation : $$\\lim_{n\\to\\infty} u_n = +\\infty.$$\n</div>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Définition 3 : Limite infinie négative</strong><br>\n$(u_n) \\to -\\infty$ si pour tout réel $A$, il existe $n_0$ tel que pour $n \\ge n_0$, $u_n < A$.<br>\nNotation : $$\\lim_{n\\to\\infty} u_n = -\\infty.$$\n</div>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Définition 4 : Suite sans limite</strong><br>\nUne suite qui oscille ou se disperse sans se rapprocher d’un nombre n’a pas de limite.<br>\n<em>Exemple :</em> $u_n = (-1)^n$.\n</div>\n<h2 style="color:#2c3e50;">III. Propriétés et théorèmes</h2>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Propriété 1 :</strong> Une suite convergente est toujours <strong>bornée</strong>.\n</div>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Propriété 2 :</strong> Si $u_n \\to +\\infty$ et $v_n \\ge u_n$ pour $n$ grand, alors $v_n \\to +\\infty$.\n</div>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Théorème de comparaison</strong><br>\nSi $u_n \\le v_n \\le w_n$ pour $n$ grand et $u_n \\to L$, $w_n \\to L$, alors $v_n \\to L$.\n</div>\n<h2 style="color:#2c3e50;">IV. Exemples et démonstrations</h2>\n<div style="background:#f6fdf4; border-left:5px solid #27ae60; padding:12px; margin:15px 0;">\n<strong>Exemple 1 :</strong> $u_n = 1/n \\to 0$<br>\nDémonstration : Pour tout $\\varepsilon>0$, choisir $n_0>1/\\varepsilon$.\nAlors $|1/n-0|<\\varepsilon$ pour $n\\ge n_0$.\n</div>\n<div style="background:#f6fdf4; border-left:5px solid #27ae60; padding:12px; margin:15px 0;">\n<strong>Exemple 2 :</strong> $v_n = n \\to +\\infty$, $w_n=-n \\to -\\infty$, $z_n=(-1)^n$ pas de limite.\n</div>\n<h2 style="color:#c0392b;">V. Erreurs fréquentes</h2>\n<div style="background:#fdeaea; border-left:5px solid #c0392b; padding:12px; margin:15px 0;">\n❌ Confondre "pas de limite" avec "tend vers +∞ ou -∞".<br>\n✔ Une suite qui croît sans limite a une limite : +∞.\n</div>\n<div style="background:#fdeaea; border-left:5px solid #c0392b; padding:12px; margin:15px 0;">\n❌ Penser que "limite nulle" signifie que les termes sont positifs.<br>\n✔ Même si $u_n$ est négative (ex : $u_n=-1/n$), la limite est 0.\n</div>\n<h2 style="color:#2c3e50;">VI. Résumé pratique</h2>\n<div style="background:#f0f0f0; border-left:5px solid #7f8c8d; padding:12px; margin:15px 0;">\n- Convergence : suite → réel L<br>\n- Divergence +∞ : suite croît sans limite<br>\n- Divergence -∞ : suite décroît sans limite<br>\n- Pas de limite : oscillation ou dispersion<br>\n- Propriétés : suite bornée si convergente, comparaison possible\n</div>\n<h2 style="color:#2c3e50;">VII. Exercices</h2>\n<ol style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px 12px 12px 30px; margin:15px 0;">\n<li>Calculer $\\lim u_n$ pour $u_n = \\frac{n+2}{2n+1}$</li>\n<li>Étudier la limite de $v_n = (-1)^n / n$</li>\n<li>Vérifier que $w_n = 3n^2 - n$ tend vers +∞</li>\n</ol>\n</div>	easy	\N	27
17	t	2025-09-04 08:54:38.196613+00	2025-09-04 08:54:38.196624+00	Calcul des limites	1	Contenu:\n<div style="background:#f9f9f9; padding:20px; border-radius:12px;">\n<h2 style="color:#2c3e50;">I. Introduction</h2>\n<p>Après avoir compris ce qu’est une limite, il est essentiel de savoir <strong>la calculer</strong> pour étudier le comportement des suites.\nOn utilisera des méthodes simples adaptées au niveau Terminale :</p>\n<ul>\n<li>Manipulation des fractions et factorisations</li>\n<li>Règles de croissance des suites usuelles</li>\n<li>Théorèmes de comparaison</li>\n</ul>\n<h2 style="color:#2980b9;">II. Limites usuelles</h2>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Limite d’une suite constante</strong><br>\nSi $u_n = k$ pour tout $n$, alors $\\lim_{n\\to\\infty} u_n = k$.<br>\n<em>Exemple :</em> $u_n = 5 \\to 5$.\n</div>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Limite d’une suite $1/n^p$</strong><br>\nPour tout $p>0$, $\\lim_{n\\to\\infty} 1/n^p = 0$.<br>\n<em>Exemple :</em> $u_n = 1/n^2 \\to 0$.\n</div>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Limite des suites polynomiales</strong><br>\nSi $u_n = a_k n^k + \\dots + a_0$, le terme de plus haut degré domine :<br>\n- Si $a_k>0$, $u_n \\to +\\infty$<br>\n- Si $a_k<0$, $u_n \\to -\\infty$<br>\n<em>Exemple :</em> $u_n = 2n^2 - 3n \\to +\\infty$.\n</div>\n<div style="background:#eaf6ff; border-left:5px solid #2980b9; padding:12px; margin:15px 0;">\n<strong>Limite des suites rationnelles</strong><br>\nPour $u_n = P(n)/Q(n)$ avec $P,Q$ polynômes :<br>\n- $\\deg(P) < \\deg(Q) \\Rightarrow u_n \\to 0$<br>\n- $\\deg(P) = \\deg(Q) \\Rightarrow u_n \\to$ rapport des coefficients principaux<br>\n- $\\deg(P) > \\deg(Q) \\Rightarrow u_n \\to \\pm\\infty$ selon le signe du terme dominant<br>\n<em>Exemple :</em> $u_n = \\frac{3n^2 + 1}{2n^2 - 5} \\to 3/2$.\n</div>\n<h2 style="color:#2c3e50;">III. Propriétés utiles pour le calcul</h2>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Propriété 1 :</strong> Limite d’une somme : $\\lim(u_n + v_n) = \\lim u_n + \\lim v_n$ (si les limites existent).\n</div>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Propriété 2 :</strong> Limite d’un produit : $\\lim(u_n \\cdot v_n) = \\lim u_n \\cdot \\lim v_n$.\n</div>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Propriété 3 :</strong> Limite d’un quotient : $\\lim(u_n/v_n) = \\lim u_n / \\lim v_n$ si $\\lim v_n \\neq 0$.\n</div>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>Propriété 4 : Théorème des gendarmes</strong><br>\nSi $u_n \\le v_n \\le w_n$ pour $n$ grand et $\\lim u_n = \\lim w_n = L$, alors $\\lim v_n = L$.\n</div>\n<h2 style="color:#2c3e50;">IV. Méthodes pratiques</h2>\n<ul>\n<li>Factoriser pour simplifier les fractions</li>\n<li>Diviser numérateur et dénominateur par le terme dominant</li>\n<li>Utiliser les limites connues des suites usuelles</li>\n<li>Appliquer le théorème des gendarmes si possible</li>\n</ul>\n<h2 style="color:#2c3e50;">V. Exemples de calcul</h2>\n<div style="background:#f6fdf4; border-left:5px solid #27ae60; padding:12px; margin:15px 0;">\n<strong>Exemple 1 :</strong> $u_n = \\frac{n+2}{2n+1} \\to 1/2$\n</div>\n<div style="background:#f6fdf4; border-left:5px solid #27ae60; padding:12px; margin:15px 0;">\n<strong>Exemple 2 :</strong> $v_n = \\frac{3n^2 + 5}{2n^3 - n} \\to 0$\n</div>\n<div style="background:#f6fdf4; border-left:5px solid #27ae60; padding:12px; margin:15px 0;">\n<strong>Exemple 3 :</strong> $w_n = \\frac{(-1)^n}{n} \\to 0$\n</div>\n<h2 style="color:#c0392b;">VI. Erreurs fréquentes</h2>\n<div style="background:#fdeaea; border-left:5px solid #c0392b; padding:12px; margin:15px 0;">\n❌ Croire que $u_n = n^2/n \\to 1$<br>\n✔ Diviser correctement : $n^2/n = n \\to +\\infty$\n</div>\n<div style="background:#fdeaea; border-left:5px solid #c0392b; padding:12px; margin:15px 0;">\n❌ Penser que $(-1)^n / n$ n’a pas de limite à cause de l’oscillation<br>\n✔ Même alternée, $(-1)^n / n \\to 0$\n</div>\n<h2 style="color:#2c3e50;">VII. Résumé pratique</h2>\n<div style="background:#f0f0f0; border-left:5px solid #7f8c8d; padding:12px; margin:15px 0;">\n- Limites des suites constantes : $k$<br>\n- Limites des suites $1/n^p$ : $0$<br>\n- Limites polynomiales et rationnelles : terme dominant ou rapport coefficients<br>\n- Propriétés : somme, produit, quotient, gendarmes<br>\n- Méthodes : factorisation, terme dominant, gendarmes\n</div>\n<h2 style="color:#2c3e50;">VIII. Exercices d’entraînement</h2>\n<ol style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px 12px 12px 30px; margin:15px 0;">\n<li>Calculer $\\lim u_n$ pour $u_n = \\frac{4n^2 + 3}{2n^2 - 5}$</li>\n<li>Étudier la limite de $v_n = \\frac{3n^3 + n}{2n^3 - 1}$</li>\n<li>Calculer $\\lim w_n = \\frac{5n - 2}{n^2 + 1}$</li>\n<li>Vérifier que $z_n = \\frac{(-1)^n}{n^2} \\to 0$</li>\n</ol>\n</div>	medium	\N	28
22	t	2025-09-07 15:24:44.433552+00	2025-09-07 15:24:44.43359+00	La démonstration par récurrence	4	<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>La <strong>démonstration par récurrence</strong> est une méthode qui permet de montrer qu’une propriété est vraie pour tous les entiers naturels.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$\\text{Si } P(0) \\text{ est vraie et } \\forall n \\in \\mathbb{N}, P(n) \\Rightarrow P(n+1), \\text{ alors } \\forall n, P(n) \\text{ est vraie}.$$\n</div>\n<p><strong>Explication :</strong> On commence par vérifier que la propriété est vraie au premier rang (initialisation), puis on montre que si elle est vraie au rang $n$, elle est également vraie au rang $n+1$ (hérédité). Cela permet de "propager" la vérité de la propriété à tous les entiers.</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Principe de la récurrence</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>La démonstration par récurrence comporte deux étapes :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n• <strong>Initialisation :</strong> Vérifier que $P(0)$ ou $P(1)$ est vraie.<br>\n• <strong>Hérédité :</strong> Montrer que $P(n) \\Rightarrow P(n+1)$.\n</div>\n<p><strong>💡 Conseil :</strong> Toujours rédiger clairement les deux étapes et conclure : « Par récurrence, la propriété est vraie pour tout entier naturel $n$. »</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Exemples détaillés</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 1 : Somme des premiers entiers</h3>\n<p><strong>Énoncé :</strong> Montrer que pour tout $n \\in \\mathbb{N}$ :</p>\n<p><strong>Données :</strong> $$1 + 2 + \\dots + n = \\frac{n(n+1)}{2}$$</p>\n<p><strong>Résolution :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li><strong>Initialisation :</strong> Pour $n=1$, $1 = \\frac{1 \\cdot 2}{2}$, vrai.</li>\n<li><strong>Hérédité :</strong> Supposons la formule vraie au rang $n$: $1+2+\\dots+n=\\frac{n(n+1)}{2}$.</li>\n<li>Au rang $n+1$ : $1+2+\\dots+n+(n+1)=\\frac{n(n+1)}{2}+(n+1)$.</li>\n<li>Simplification : $\\frac{n(n+1)+2(n+1)}{2} = \\frac{(n+1)(n+2)}{2}$.</li>\n</ul>\n</div>\n<div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>Résultat final :</strong> La formule est vraie pour tout $n \\in \\mathbb{N}$.\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 2 : Suite croissante</h3>\n<p><strong>Situation :</strong> Soit la suite $(u_n)$ définie par $u_0=1$ et $u_{n+1}=u_n+2$. Montrons que $u_n \\geq 1$ pour tout $n$.</p>\n<p><strong>Calculs :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li><strong>Initialisation :</strong> $u_0=1 \\geq 1$, vrai.</li>\n<li><strong>Hérédité :</strong> Supposons $u_n \\geq 1$, alors $u_{n+1}=u_n+2 \\geq 1+2 = 3 \\geq 1$.</li>\n</ul>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Vérification :</strong> La propriété est vraie pour tout $n \\in \\mathbb{N}$.\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. Méthode générale</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Étapes à suivre</h3>\n<p>Pour appliquer la récurrence :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$\\text{Initialisation} \\; P(0) \\quad \\text{Hérédité} \\; P(n)\\Rightarrow P(n+1) \\quad \\Longrightarrow P(n), \\forall n$$\n</div>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>💡 Démarche :</strong><br>\n• Identifier la propriété $P(n)$.<br>\n• Vérifier l’initialisation.<br>\n• Démontrer l’hérédité.<br>\n• Conclure rigoureusement.\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">V. Propriétés et caractéristiques</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin:0; padding-left:20px;">\n<li><strong>Propriété 1 :</strong> La récurrence est adaptée aux suites et formules sur les entiers naturels.</li>\n<li><strong>Propriété 2 :</strong> C’est une méthode universelle et rigoureuse.</li>\n<li><strong>Propriété 3 :</strong> On peut utiliser des récurrences simples ou fortes selon les cas.</li>\n<li><strong>Aspect graphique :</strong> La propagation de la propriété peut se visualiser comme une chaîne de dominos.</li>\n</ul>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">VI. Erreurs fréquentes et conseils</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;">\n<strong>❌ Pièges :</strong>\n<ul style="margin:0; padding-left:20px;">\n<li>Oublier l’initialisation.</li>\n<li>Confondre hypothèse et conclusion.</li>\n<li>Ne pas conclure clairement.</li>\n</ul>\n</div>\n<div style="background:#f0f9f0; padding:12px; border-radius:4px;">\n<strong>✅ Conseils :</strong>\n<ul style="margin:0; padding-left:20px;">\n<li>Identifier clairement $P(n)$ avant de commencer.</li>\n<li>Rédiger distinctement initialisation, hérédité, conclusion.</li>\n<li>S’entraîner sur des exemples simples pour bien comprendre le mécanisme.</li>\n</ul>\n</div>\n</div>\n</div>	medium	\N	32
20	t	2025-09-07 14:52:00.573686+00	2025-09-07 14:52:00.573768+00	Étude des variations et de la monotonie des suites numériques	4	<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition d'une suite monotone</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Une <strong>suite numérique</strong> est une fonction définie sur $\\mathbb{N}$ (ou sur un sous-ensemble de $\\mathbb{N}$) à valeurs dans $\\mathbb{R}$.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Définitions mathématiques :</strong><br>\nSuite <strong>croissante</strong> : $\\forall n \\in \\mathbb{N}, \\quad U_n \\leq U_{n+1}$<br>\nSuite <strong>décroissante</strong> : $\\forall n \\in \\mathbb{N}, \\quad U_n \\geq U_{n+1}$<br>\nSuite <strong>constante</strong> : $\\forall n \\in \\mathbb{N}, \\quad U_n = U_0$\n</div>\n<p><strong>Explication :</strong> L'étude de la monotonie permet de comprendre le comportement global d'une suite.</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Méthodes d'étude du sens de variation</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Il existe <strong>deux méthodes principales</strong> pour déterminer si une suite est monotone :</p>\n<div style="margin:15px 0;">\n<h4 style="color:#34495e; margin:10px 0;">Méthode 1 : Étude de $U_{n+1} - U_n$</h4>\n<div style="text-align:center; font-size:1.1em; margin:10px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\nÉtudier le signe de $U_{n+1} - U_n$ :<br>\n• Si $U_{n+1} - U_n \\geq 0$ pour tout $n$ : suite croissante<br>\n• Si $U_{n+1} - U_n \\leq 0$ pour tout $n$ : suite décroissante<br>\n• Si $U_{n+1} - U_n = 0$ pour tout $n$ : suite constante\n</div>\n</div>\n<div style="margin:15px 0;">\n<h4 style="color:#34495e; margin:10px 0;">Méthode 2 : Étude du rapport $U_{n+1}/U_n$</h4>\n<div style="text-align:center; font-size:1.1em; margin:10px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\nPour les suites de terme général positif :<br>\nÉtudier le signe de $U_{n+1}/U_n - 1$ :<br>\n• Si $U_{n+1}/U_n \\geq 1$ pour tout $n$ : suite croissante<br>\n• Si $U_{n+1}/U_n \\leq 1$ pour tout $n$ : suite décroissante<br>\n• Si $U_{n+1}/U_n = 1$ pour tout $n$ : suite constante\n</div>\n</div>\n<div style="background:#fff8e6; border-left:5px solid #e67e22; padding:12px; margin:15px 0;">\n<strong>💡 Conseils méthodologiques :</strong><br>\n• Choisissez la méthode la plus adaptée à l'expression de la suite<br>\n• Pour les suites définies par récurrence $U_{n+1} = f(U_n)$, étudiez $f(x) - x$<br>\n• Pour les suites géométriques, privilégiez le rapport\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Exemples détaillés</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 1 : Suite arithmétique (méthode différence)</h3>\n<p><strong>Énoncé :</strong> Étudier la monotonie de $U_n = 3n - 1$</p>\n<p><strong>Données :</strong> Suite arithmétique de raison $r = 3$</p>\n<p><strong>Résolution :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$U_n = 3n - 1$</li>\n<li>$U_{n+1} = 3(n+1) - 1 = 3n + 3 - 1 = 3n + 2$</li>\n<li>$U_{n+1} - U_n = (3n + 2) - (3n - 1) = 3$</li>\n<li>$U_{n+1} - U_n = 3 > 0$ pour tout $n \\in \\mathbb{N}$</li>\n</ul>\n</div>\n<div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>Résultat final :</strong> La suite est strictement croissante car la raison $r = 3 > 0$\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 2 : Suite géométrique (méthode rapport)</h3>\n<p><strong>Situation :</strong> Analyser la monotonie de $V_n = 2 \\times (0.8)^n$</p>\n<div style="text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$V_n = 2 \\times \\left(\\frac{4}{5}\\right)^n$$\n</div>\n<p><strong>Calculs détaillés :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$V_0 = 2 \\times 1 = 2$</li>\n<li>$V_1 = 2 \\times \\frac{4}{5} = 1.6$</li>\n<li>$V_2 = 2 \\times \\frac{16}{25} = 1.28$</li>\n<li>$V_{n+1} = \\frac{4}{5} V_n$</li>\n<li>$\\frac{V_{n+1}}{V_n} = \\frac{4}{5} = 0.8$</li>\n<li>$\\frac{V_{n+1}}{V_n} = 0.8 < 1$ pour tout $n \\in \\mathbb{N}$</li>\n</ul>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Vérification :</strong> Rapport $q = 4/5 < 1$ ⇒ suite décroissante\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 3 : Suite par récurrence (méthode différence)</h3>\n<p><strong>Situation :</strong> Étudier $U_0 = 1$ et $U_{n+1} = \\sqrt{U_n + 1}$ pour $n \\geq 1$</p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>Calculs détaillés :</strong>\n<div style="margin:8px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$U_0 = 1$</li>\n<li>$U_1 = \\sqrt{1 + 1} = \\sqrt{2} \\approx 1.414$</li>\n<li>$U_2 = \\sqrt{\\sqrt{2} + 1} \\approx \\sqrt{2.414} \\approx 1.554$</li>\n<li>$U_3 = \\sqrt{\\sqrt{\\sqrt{2} + 1} + 1} \\approx \\sqrt{2.554} \\approx 1.598$</li>\n</ul>\n</div>\n</div>\n<p><strong>Analyse :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$U_{n+1} - U_n = \\sqrt{U_n + 1} - U_n$</li>\n<li>Étudions $f(x) = \\sqrt{x + 1} - x$</li>\n<li>$f'(x) = \\frac{1}{2\\sqrt{x + 1}} - 1$</li>\n<li>$f'(x) = 0$ pour $x = 1/4$</li>\n<li>$f'(x) > 0$ pour $x \\in ]0, 1/4[, \\quad f'(x) < 0$ pour $x \\in ]1/4, +\\infty[$</li>\n<li>$f(x) \\geq f(1/4) = \\sqrt{5/4} - 1/4 = \\frac{\\sqrt{5}}{2} - \\frac{1}{4} > 0$</li>\n</ul>\n</div>\n<div style="background:#e8f5e8; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>✅ Conclusion :</strong> $U_{n+1} - U_n \\geq \\frac{\\sqrt{5}}{2} - \\frac{1}{4} > 0$ ⇒ suite strictement croissante\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. Théorème de convergence monotone</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Théorème fondamental</h3>\n<p>Ce théorème est essentiel pour prouver la convergence des suites monotones.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Théorème de convergence monotone :</strong><br>\nToute suite monotone bornée converge<br>\n• Suite croissante majorée ⇒ convergente<br>\n• Suite décroissante minorée ⇒ convergente\n</div>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>💡 Démarche à suivre :</strong><br>\n• Prouver que la suite est monotone<br>\n• Prouver qu'elle est bornée (majorée si croissante, minorée si décroissante)<br>\n• Conclure à la convergence\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Application pratique</h3>\n<p><strong>Problème :</strong> Montrer que la suite définie par $U_0 = 1$ et $U_{n+1} = \\sqrt{2 + U_n}$ converge</p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>Éléments donnés :</strong><br>\n• Suite définie par récurrence<br>\n• Étude de monotonie et bornitude<br>\n• Application du théorème de convergence monotone\n</div>\n<div style="text-align:center; margin:15px 0;">\n<strong>Résolution :</strong>\n<div style="font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;">\nMonotonie : $U_{n+1} - U_n = \\sqrt{2 + U_n} - U_n$<br>\nÉtudions $f(x) = \\sqrt{2 + x} - x$<br>\n$f'(x) = \\frac{1}{2\\sqrt{2 + x}} - 1 = \\frac{1 - 2\\sqrt{2 + x}}{2\\sqrt{2 + x}}$<br>\n$f'(x) \\leq 0$ pour $x \\geq 2$<br>\nBornitude : $\\forall n \\in \\mathbb{N}, \\quad U_n \\leq 2$ (majorée)<br>\n<strong>Conclusion :</strong> Suite croissante majorée ⇒ convergente\n</div>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Solution finale :</strong> La suite converge vers la limite $L$ vérifiant $L = \\sqrt{2 + L}$\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">V. Propriétés et caractéristiques</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin:0; padding-left:20px;">\n<li><strong>Stabilité par addition :</strong> La somme de deux suites monotones de même sens est monotone</li>\n<li><strong>Stabilité par multiplication :</strong> Le produit de deux suites monotones positives est monotone</li>\n<li><strong>Propriété des suites arithmétiques :</strong> Une suite arithmétique est monotone si et seulement si sa raison est positive (croissante) ou négative (décroissante)</li>\n<li><strong>Propriété des suites géométriques :</strong> Une suite géométrique est monotone si et seulement si son rapport est positif et vérifie $q \\geq 1$ (croissante) ou $0 < q \\leq 1$ (décroissante)</li>\n<li><strong>Conservation par composition :</strong> Si $f$ est croissante et $U_n$ est croissante, alors $f(U_n)$ est croissante</li>\n<li><strong>Lien avec les fonctions réciproques :</strong> Toute suite strictement monotone admet une fonction réciproque définie sur son image</li>\n<li><strong>Comportement asymptotique :</strong> Étude de la limite selon le type de suite et sa monotonie</li>\n<li><strong>Bornitude et convergence :</strong> Une suite monotone bornée converge toujours</li>\n</ul>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">VI. Erreurs fréquentes et conseils</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;">\n<strong>❌ Pièges à éviter :</strong>\n<div style="margin:8px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>Confondre suite monotone et suite convergente</li>\n<li>Oublier de vérifier la bornitude pour conclure à la convergence</li>\n<li>Se tromper dans le calcul de $U_{n+1} - U_n$</li>\n<li>Mélanger les méthodes (différence et rapport)</li>\n<li>Utiliser le rapport $U_{n+1}/U_n$ pour des suites pouvant être négatives</li>\n<li>Ne pas vérifier le domaine de définition de la suite</li>\n<li>Confondre les indices $U_n$ et $U_{n+1}$ dans les calculs</li>\n</ul>\n</div>\n</div>\n<div style="background:#f0f9f0; padding:12px; border-radius:4px;">\n<strong>✅ Conseils méthodologiques :</strong>\n<div style="margin:8px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>Commencez toujours par calculer quelques termes pour observer le comportement</li>\n<li>Choisissez la méthode appropriée selon l'expression de la suite</li>\n<li>Pour les suites géométriques, privilégiez le rapport $U_{n+1}/U_n$</li>\n<li>Vérifiez systématiquement $U_{n+1} - U_n$ ou $U_{n+1}/U_n$ sur plusieurs indices</li>\n<li>Utilisez le théorème de convergence monotone quand c'est approprié</li>\n<li>Pour les suites définies par récurrence, étudiez toujours $f(x) - x$</li>\n<li>Vérifiez la positivité des termes avant d'utiliser le rapport</li>\n<li>Tracez un tableau des premiers termes pour visualiser la tendance</li>\n</ul>\n</div>\n</div>\n</div>\n</div>	medium	\N	25
21	t	2025-09-07 14:58:07.040237+00	2025-09-07 14:58:07.040257+00	Étude des limites et de la convergence des suites numériques	5	<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition de la limite d'une suite</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Une <strong>suite numérique</strong> converge vers une limite $L$ si, à partir d'un certain rang, tous ses termes sont aussi proches que l'on veut de $L$.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Définition mathématique :</strong><br>\n$\\lim_{n \\to +\\infty} U_n = L \\quad \\Longleftrightarrow \\quad \\forall \\varepsilon > 0, \\quad \\exists N \\in \\mathbb{N}, \\quad \\forall n \\geq N, \\quad |U_n - L| < \\varepsilon$<br>\n$\\lim_{n \\to +\\infty} U_n = +\\infty \\quad \\Longleftrightarrow \\quad \\forall A > 0, \\quad \\exists N \\in \\mathbb{N}, \\quad \\forall n \\geq N, \\quad U_n > A$<br>\n$\\lim_{n \\to +\\infty} U_n = -\\infty \\quad \\Longleftrightarrow \\quad \\forall A < 0, \\quad \\exists N \\in \\mathbb{N}, \\quad \\forall n \\geq N, \\quad U_n < A$\n</div>\n<p><strong>Explication :</strong> La convergence signifie que les termes de la suite se rapprochent indéfiniment d'une valeur limite, finie ou infinie.</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Théorèmes fondamentaux sur les limites</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Les théorèmes sur les limites permettent de calculer facilement les limites de suites complexes.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Opérations sur les limites :</strong><br>\nSi $\\lim U_n = L$ et $\\lim V_n = M$, alors :<br>\n$\\lim (U_n + V_n) = L + M \\quad \\quad \\lim (U_n \\times V_n) = L \\times M$<br>\n$\\lim \\left(\\frac{U_n}{V_n}\\right) = \\frac{L}{M}$ si $M \\neq 0 \\quad \\quad \\lim (k \\times U_n) = k \\times L$<br>\n$\\lim U_n^p = L^p$ si $p \\in \\mathbb{N}$ et $L \\geq 0$\n</div>\n<p><strong>💡 Conseil important :</strong> Les opérations sur les limites suivent les mêmes règles que pour les nombres réels.</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Exemples détaillés</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 1 : Suite arithmétique</h3>\n<p><strong>Énoncé :</strong> Calculer la limite de $U_n = \\frac{3n + 1}{2n + 4}$</p>\n<p><strong>Données :</strong> Suite rationnelle en $n$</p>\n<p><strong>Résolution :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$U_n = \\frac{3n + 1}{2n + 4} = \\frac{3 + \\frac{1}{n}}{2 + \\frac{4}{n}}$</li>\n<li>Quand $n \\to +\\infty$, $\\frac{1}{n} \\to 0$ et $\\frac{4}{n} \\to 0$</li>\n<li>Donc $U_n \\to \\frac{3 + 0}{2 + 0} = \\frac{3}{2}$</li>\n<li>$\\lim_{n \\to +\\infty} U_n = \\frac{3}{2}$</li>\n</ul>\n</div>\n<div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>Résultat final :</strong> La suite converge vers $\\frac{3}{2}$\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 2 : Suite géométrique</h3>\n<p><strong>Situation :</strong> Étudier la limite de $V_n = 2 \\times \\left(\\frac{3}{4}\\right)^n$</p>\n<div style="text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$V_n = 2 \\times q^n \\quad \\text{avec} \\quad q = \\frac{3}{4}$$\n</div>\n<p><strong>Calculs détaillés :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$V_n = 2 \\times \\left(\\frac{3}{4}\\right)^n$</li>\n<li>Comme $|q| = \\frac{3}{4} < 1$, alors $q^n \\to 0$ quand $n \\to +\\infty$</li>\n<li>Donc $V_n \\to 2 \\times 0 = 0$</li>\n<li>$\\lim_{n \\to +\\infty} V_n = 0$</li>\n</ul>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Vérification :</strong> $|q| < 1$ ⇒ suite géométrique convergente vers 0\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 3 : Suite exponentielle</h3>\n<p><strong>Situation :</strong> Calculer $\\lim_{n \\to +\\infty} \\left(1 + \\frac{1}{n}\\right)^n$</p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>Calculs détaillés :</strong>\n<div style="margin:8px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$U_n = \\left(1 + \\frac{1}{n}\\right)^n$</li>\n<li>Cette expression définit le nombre $e$</li>\n<li>$\\lim_{n \\to +\\infty} U_n = e \\approx 2.718$</li>\n</ul>\n</div>\n</div>\n<p><strong>Propriété :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>Pour tout $x \\in \\mathbb{R}$, $\\lim_{n \\to +\\infty} \\left(1 + \\frac{x}{n}\\right)^n = e^x$</li>\n<li>Cette formule est fondamentale en analyse</li>\n</ul>\n</div>\n<div style="background:#e8f5e8; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>✅ Conclusion :</strong> Cette suite converge vers le nombre $e$\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. Méthodes de calcul des limites</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Méthode de comparaison</h3>\n<p>Pour déterminer la limite d'une suite, on peut la comparer à une suite de limite connue.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Théorème de comparaison :</strong><br>\nSi $U_n \\leq V_n \\leq W_n$ pour $n$ assez grand,<br>\net si $\\lim U_n = L$ et $\\lim W_n = L$,<br>\nalors $\\lim V_n = L$\n</div>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>💡 Démarche à suivre :</strong><br>\n• Majorer et minorer la suite par des suites de limite connue<br>\n• Utiliser les théorèmes d'encadrement<br>\n• Conclure par théorème de comparaison\n</div>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Application pratique</h3>\n<p><strong>Problème :</strong> Calculer $\\lim_{n \\to +\\infty} \\frac{n^2 + 3n}{2n^2 - n + 1}$</p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>Éléments donnés :</strong><br>\n• Suite rationnelle<br>\n• Degré du numérateur = degré du dénominateur<br>\n• Méthode de comparaison par équivalent\n</div>\n<div style="text-align:center; margin:15px 0;">\n<strong>Résolution :</strong>\n<div style="font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;">\n$\\frac{n^2 + 3n}{2n^2 - n + 1} = \\frac{n^2(1 + \\frac{3}{n})}{n^2(2 - \\frac{1}{n} + \\frac{1}{n^2})} = \\frac{1 + \\frac{3}{n}}{2 - \\frac{1}{n} + \\frac{1}{n^2}}$<br>\nQuand $n \\to +\\infty$ : $\\frac{1 + 0}{2 - 0 + 0} = \\frac{1}{2}$<br>\n<strong>Conclusion :</strong> $\\lim_{n \\to +\\infty} \\frac{n^2 + 3n}{2n^2 - n + 1} = \\frac{1}{2}$\n</div>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Solution finale :</strong> La suite converge vers $\\frac{1}{2}$\n</div>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">V. Propriétés et caractéristiques</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin:0; padding-left:20px;">\n<li><strong>Unicité de la limite :</strong> Une suite ne peut converger que vers une seule limite</li>\n<li><strong>Limite et inégalités :</strong> Si $U_n \\leq V_n$ et $\\lim U_n = L$, $\\lim V_n = M$, alors $L \\leq M$</li>\n<li><strong>Limite infinie :</strong> Une suite diverge vers $+\\infty$ (resp. $-\\infty$) si elle devient arbitrairement grande (resp. petite)</li>\n<li><strong>Aspect graphique :</strong> Les termes d'une suite convergente se rapprochent de la droite horizontale d'équation $y = L$</li>\n<li><strong>Continuité séquentielle :</strong> Les fonctions usuelles sont continues pour les suites</li>\n<li><strong>Comportement asymptotique :</strong> Étude du comportement de la suite quand $n$ devient très grand</li>\n</ul>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">VI. Erreurs fréquentes et conseils</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;">\n<strong>❌ Pièges à éviter :</strong>\n<div style="margin:8px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>Confondre convergence et divergence</li>\n<li>Oublier que la limite infinie n'est pas une limite finie</li>\n<li>Diviser par zéro dans les calculs de limites</li>\n<li>Appliquer les opérations sur les limites sans vérifier les conditions</li>\n<li>Utiliser la forme indéterminée $0 \\times \\infty$ sans transformation</li>\n<li>Ne pas simplifier les fractions rationnelles avant de calculer la limite</li>\n<li>Confondre les cas où le degré du numérateur est supérieur/inférieur/égal à celui du dénominateur</li>\n</ul>\n</div>\n</div>\n<div style="background:#f0f9f0; padding:12px; border-radius:4px;">\n<strong>✅ Conseils méthodologiques :</strong>\n<div style="margin:8px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>Commencez toujours par identifier le type de suite (arithmétique, géométrique, rationnelle, etc.)</li>\n<li>Pour les fractions rationnelles, comparez les degrés du numérateur et du dénominateur</li>\n<li>Utilisez les formes indéterminées classiques : $\\frac{0}{0}$, $\\frac{\\infty}{\\infty}$, $0 \\times \\infty$, $\\infty - \\infty$</li>\n<li>Factorisez et simplifiez avant de calculer la limite</li>\n<li>Pour les suites géométriques, vérifiez toujours si $|q| < 1$</li>\n<li>Utilisez les théorèmes d'encadrement pour prouver la convergence</li>\n<li>Vérifiez systématiquement si la suite est définie pour tout $n$ assez grand</li>\n<li>Tracez un tableau des premiers termes pour visualiser le comportement</li>\n</ul>\n</div>\n</div>\n</div>\n</div>	medium	\N	26
25	t	2025-09-15 14:05:51.289477+00	2025-09-15 14:05:51.289493+00	Définition et notions de base sur les suites numériques	0	<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Une <strong>suite numérique</strong> est une liste ordonnée de nombres, chaque nombre étant repéré par un indice entier $n$ appelé <em>rang</em>.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$(u_n)_{n \\in \\mathbb{N}}$$\n</div>\n<p><strong>Explication :</strong> Chaque terme de la suite est noté $u_n$, où $n$ indique la position du terme dans la suite. Une suite peut être finie (nombre limité de termes) ou infinie (définie pour tout $n \\in \\mathbb{N}$).</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Deux façons de définir une suite</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3>1) Définition explicite</h3>\n<p>Une suite est donnée directement par une formule qui permet de calculer chaque terme à partir de son rang $n$.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_n = f(n)$$\n</div>\n<p><strong>💡 Exemple :</strong> $u_n = 3n + 2$<br>\nPour calculer les premiers termes :</p>\n<ul style="margin-left:20px;">\n<li>$u_0 = 3 \\times 0 + 2 = 2$</li>\n<li>$u_1 = 3 \\times 1 + 2 = 5$</li>\n<li>$u_2 = 3 \\times 2 + 2 = 8$</li>\n<li>$u_3 = 3 \\times 3 + 2 = 11$</li>\n<li>$u_4 = 3 \\times 4 + 2 = 14$</li>\n</ul>\n<p>La suite est donc : $2, 5, 8, 11, 14, ...$. On peut calculer n’importe quel terme directement, par exemple $u_{10} = 32$.</p>\n</div>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3>2) Définition par récurrence</h3>\n<p>Une suite peut être définie par son premier terme et une relation qui permet de passer de $u_n$ à $u_{n+1}$.</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_{n+1} = f(u_n)$$\n</div>\n<p><strong>💡 Exemple :</strong> $u_0 = 1$, et $u_{n+1} = u_n + 3$</p>\n<ul style="margin-left:20px;">\n<li>$u_0 = 1$</li>\n<li>$u_1 = u_0 + 3 = 4$</li>\n<li>$u_2 = u_1 + 3 = 7$</li>\n<li>$u_3 = u_2 + 3 = 10$</li>\n<li>$u_4 = u_3 + 3 = 13$</li>\n</ul>\n<p>La suite est donc : $1, 4, 7, 10, 13, ...$. Chaque terme dépend du précédent.</p>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Vocabulaire clé</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin-left:20px;">\n<li><strong>Terme initial :</strong> $u_0$ ou $u_1$ selon le point de départ.</li>\n<li><strong>Rang :</strong> l’indice $n$ qui repère chaque terme $u_n$.</li>\n<li><strong>Terme général :</strong> la formule donnant $u_n$ en fonction de $n$.</li>\n<li><strong>Suite finie :</strong> suite avec un nombre limité de termes.</li>\n<li><strong>Suite infinie :</strong> suite définie pour tout $n \\in \\mathbb{N}$.</li>\n</ul>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. Exemples classiques de suites</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin-left:20px;">\n<li><strong>Suite des carrés :</strong> $u_n = n^2$ → $0, 1, 4, 9, 16, ...$</li>\n<li><strong>Suite arithmétique :</strong> $u_{n+1} = u_n + r$<br>\nExemple : $u_0=0$, $r=2$ → $0, 2, 4, 6, ...$</li>\n<li><strong>Suite géométrique :</strong> $u_{n+1} = q \\cdot u_n$<br>\nExemple : $u_0=1$, $q=2$ → $1, 2, 4, 8, 16, ...$</li>\n</ul>\n</div>\n<h2 style="color:#2c3e50; border-bottom:2px solid #c0392b; padding-bottom:8px;">V. Erreurs fréquentes et conseils</h2>\n<div style="background:#fdeaea; border-left:5px solid #c0392b; padding:12px; margin:15px 0; border-radius:6px;">\n<strong>❌ Pièges à éviter :</strong>\n<ul style="margin-left:20px;">\n<li>Confondre le terme $u_n$ avec la suite entière $(u_n)$.</li>\n<li>Penser que l’indice commence toujours à 1.</li>\n<li>Oublier que certaines suites sont définies par récurrence et non explicitement.</li>\n</ul>\n</div>\n<div style="background:#f0f9f0; padding:12px; border-radius:6px; margin-bottom:10px;">\n<strong>✅ Conseils méthodologiques :</strong>\n<ul style="margin-left:20px;">\n<li>Identifier d’abord si la suite est définie explicitement ou par récurrence.</li>\n<li>Vérifier toujours le terme initial et l’indice de départ.</li>\n<li>Pour calculer plusieurs termes, procéder étape par étape.</li>\n</ul>\n</div>\n</div>	easy	\N	22
18	t	2025-09-06 20:54:26.928017+00	2025-09-15 14:13:09.712783+00	Les suites arithmétiques	2	<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Une <strong>suite arithmétique</strong> est une suite numérique $(u_n)$ dans laquelle chaque terme, à partir du second, s'obtient en ajoutant une constante <strong>r</strong> appelée <em>raison</em> :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_{n+1} = u_n + r$$\n</div>\n<p>Le premier terme est noté <strong>$u_0$</strong> (ou $u_1$ selon le point de départ).</p>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Terme général</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Le terme de rang <em>n</em> d'une suite arithmétique se calcule directement avec :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_n = u_0 + n \\cdot r$$\n</div>\n<p>Cette formule permet de connaître n'importe quel terme sans calculer tous les précédents.</p>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Exemples détaillés</h2>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 1 : Construction progressive</h3>\n<p><strong>Données :</strong> Premier terme $u_0 = 3$, raison $r = 2$</p>\n<p><strong>Calculs étape par étape :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$u_0 = 3$ (point de départ)</li>\n<li>$u_1 = u_0 + r = 3 + 2 = 5$</li>\n<li>$u_2 = u_1 + r = 5 + 2 = 7$</li>\n<li>$u_3 = u_2 + r = 7 + 2 = 9$</li>\n<li>$u_4 = u_3 + r = 9 + 2 = 11$</li>\n</ul>\n</div>\n<div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>Suite complète :</strong> 3, 5, 7, 9, 11, 13, 15, ...\n</div>\n</div>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 2 : Terme général en action</h3>\n<p>Pour la même suite ($u_0 = 3$, $r = 2$), appliquons la formule :</p>\n<div style="text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_n = 3 + 2n$$\n</div>\n<p><strong>Calculs directs :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$u_5 = 3 + 2 \\times 5 = 13$</li>\n<li>$u_{10} = 3 + 2 \\times 10 = 23$</li>\n</ul>\n</div>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. Comment calculer la somme des termes ?</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Formule principale de la somme</h3>\n<p>Pour additionner les <strong>n+1</strong> premiers termes d'une suite arithmétique, on utilise :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Somme des (n+1) premiers termes :</strong><br>\n$$S_n = \\frac{(n+1)(u_0 + u_n)}{2}$$\n</div>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>💡 Méthode intuitive :</strong><br>\n• Moyenne des extrémités : $(u_0 + u_n)/2$<br>\n• Multiplier par le nombre de termes : $n+1$<br>\n• Résultat = somme des termes\n</div>\n</div>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple concret</h3>\n<p><strong>Situation :</strong> Calculer la somme des 5 premiers termes : 3, 5, 7, 9, 11</p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>Données :</strong><br>\n• Nombre de termes : $5$ → donc $n = 4$<br>\n• Premier terme : $u_0 = 3$<br>\n• Dernier terme : $u_4 = 11$\n</div>\n<div style="text-align:center; margin:15px 0;">\n<strong>Application :</strong>\n<div style="font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;">\n$$S_4 = \\frac{(4+1)(3+11)}{2} = \\frac{5 \\times 14}{2} = 35$$\n</div>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Vérification :</strong> 3 + 5 + 7 + 9 + 11 = 35 ✓\n</div>\n</div>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Formule alternative (avec la raison)</h3>\n<p>Si on connaît seulement $u_0$ et $r$ :</p>\n<div style="text-align:center; font-size:1.1em; margin:10px 0; padding:10px; background:#f8f9fa; border-radius:4px;">\n$$S_n = \\frac{(n+1)}{2} \\cdot (2 u_0 + n \\cdot r)$$\n</div>\n<p><strong>Pour notre exemple :</strong> $u_0 = 3$, $r = 2$, $n = 4$</p>\n<div style="font-size:1em; margin:10px 0; padding:8px; background:#ecf0f1; border-radius:4px;">\n$$S_4 = \\frac{5}{2} \\cdot (2 \\times 3 + 4 \\times 2) = \\frac{5}{2} \\cdot 14 = 35$$\n</div>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">V. Propriétés importantes</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin:0; padding-left:20px;">\n<li>Si $r > 0$, la suite est <strong>croissante</strong></li>\n<li>Si $r < 0$, la suite est <strong>décroissante</strong></li>\n<li>Si $r = 0$, la suite est <strong>constante</strong></li>\n<li>Graphiquement, $(u_n)$ forme une droite avec points régulièrement espacés</li>\n</ul>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">VI. Erreurs fréquentes</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;">\n<strong>❌ À éviter :</strong>\n<ul style="margin:8px 0; padding-left:20px;">\n<li>Oublier que l'indexation peut commencer à $u_0$ ou $u_1$</li>\n<li>Confondre la formule du terme général et celle de la somme</li>\n<li>Calculer terme par terme au lieu d'utiliser les formules</li>\n</ul>\n</div>\n<div style="background:#f0f9f0; padding:12px; border-radius:4px;">\n<strong>✅ Conseils :</strong>\n<ul style="margin:8px 0; padding-left:20px;">\n<li>Identifier toujours $u_0$ et la raison $r$</li>\n<li>Choisir la formule adaptée aux données disponibles</li>\n<li>Vérifier les résultats avec des valeurs simples</li>\n</ul>\n</div>\n</div>\n\n</div>	easy	\N	23
19	t	2025-09-07 13:08:24.400525+00	2025-09-15 14:19:54.092803+00	Les suites géométriques	3	<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition d'une suite géométrique</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Une <strong>suite géométrique</strong> est une suite numérique $(u_n)$ dans laquelle chaque terme, à partir du second, s'obtient en multipliant le terme précédent par une constante <strong>q</strong> appelée <em>raison géométrique</em> :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_{n+1} = u_n \\cdot q$$\n</div>\n<p><strong>Explication simple :</strong> Pour passer du terme de rang $n$ au terme suivant ($n+1$), on multiplie toujours par la même valeur $q$.</p>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Comment calculer n'importe quel terme ?</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<p>Le terme de rang $n$ d'une suite géométrique se calcule directement avec :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_n = u_0 \\cdot q^n$$\n</div>\n<p><strong>💡 Conseil :</strong> Cette formule permet de "sauter" directement au terme souhaité !</p>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Exemples concrets et détaillés</h2>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 1 : Construction progressive</h3>\n<p><strong>Données :</strong> Premier terme $u_0 = 2$, raison $q = 3$</p>\n<p><strong>Calculs étape par étape :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$u_0 = 2$ (point de départ)</li>\n<li>$u_1 = u_0 \\cdot q = 2 \\cdot 3 = 6$</li>\n<li>$u_2 = u_1 \\cdot q = 6 \\cdot 3 = 18$</li>\n<li>$u_3 = u_2 \\cdot q = 18 \\cdot 3 = 54$</li>\n<li>$u_4 = u_3 \\cdot q = 54 \\cdot 3 = 162$</li>\n</ul>\n</div>\n<div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;">\n<strong>Suite complète :</strong> 2, 6, 18, 54, 162, 486, ...\n</div>\n</div>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple 2 : Terme général en action</h3>\n<p>Pour la même suite ($u_0 = 2$, $q = 3$), appliquons la formule :</p>\n<div style="text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n$$u_n = 2 \\cdot 3^n$$\n</div>\n<p><strong>Calculs directs :</strong></p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<ul style="margin:0; padding-left:20px;">\n<li>$u_5 = 2 \\cdot 3^5 = 2 \\cdot 243 = 486$</li>\n<li>$u_6 = 2 \\cdot 3^6 = 2 \\cdot 729 = 1458$</li>\n</ul>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Vérification :</strong> Chaque terme est bien multiplié par $q=3$\n</div>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. Comment calculer la somme des termes ?</h2>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Formule principale de la somme</h3>\n<p>Pour additionner les <strong>n+1</strong> premiers termes d'une suite géométrique de raison $q \\neq 1$, on utilise :</p>\n<div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">\n<strong>Somme des (n+1) premiers termes :</strong><br>\n$$S_n = u_0 \\cdot \\frac{1-q^{n+1}}{1-q}$$\n</div>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>💡 Méthode intuitive :</strong><br>\n• On utilise la formule des sommes géométriques<br>\n• Le facteur $(1-q)$ au dénominateur vient de la raison<br>\n• C'est beaucoup plus rapide que d'additionner terme par terme !\n</div>\n</div>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Exemple concret</h3>\n<p><strong>Situation :</strong> Calculer la somme des 5 premiers termes de la suite : 2, 6, 18, 54, 162</p>\n<div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">\n<strong>Données identifiées :</strong><br>\n• Nombre de termes : $5$ → donc $n = 4$<br>\n• Premier terme : $u_0 = 2$<br>\n• Raison : $q = 3$\n</div>\n<div style="text-align:center; margin:15px 0;">\n<strong>Application :</strong>\n<div style="font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;">\n$$S_4 = 2 \\cdot \\frac{1-3^5}{1-3} = 2 \\cdot \\frac{1-243}{-2} = 2 \\cdot 121 = 242$$\n</div>\n</div>\n<div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">\n<strong>✅ Vérification :</strong> 2 + 6 + 18 + 54 + 162 = 242 ✓\n</div>\n</div>\n\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<h3 style="color:#34495e; margin-top:0;">Cas particulier : raison $q = 1$</h3>\n<p>Si $q = 1$, la suite est constante et la somme devient :</p>\n<div style="text-align:center; font-size:1.1em; margin:10px 0; padding:10px; background:#f8f9fa; border-radius:4px;">\n$$S_n = u_0 \\cdot (n+1)$$\n</div>\n<p><strong>Exemple :</strong> Suite 5, 5, 5, 5, 5 → $S_4 = 5 \\times 5 = 25$</p>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">V. Propriétés importantes à retenir</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<ul style="margin:0; padding-left:20px;">\n<li><strong>Si $q > 1$ :</strong> la suite est <strong>croissante</strong></li>\n<li><strong>Si $0 < q < 1$ :</strong> la suite est <strong>décroissante</strong></li>\n<li><strong>Si $q = 1$ :</strong> la suite est <strong>constante</strong></li>\n<li><strong>Si $q < 0$ :</strong> la suite <strong>oscille</strong> (alternance des signes)</li>\n<li><strong>Représentation graphique :</strong> Les points forment une courbe exponentielle</li>\n</ul>\n</div>\n\n<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">VI. Erreurs fréquentes à éviter</h2>\n<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">\n<div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;">\n<strong>❌ À éviter :</strong>\n<ul style="margin:8px 0; padding-left:20px;">\n<li>Oublier que l'indexation peut commencer à $u_0$ ou $u_1$</li>\n<li>Confondre la formule de somme avec $q=1$ et $q \\neq 1$</li>\n<li>Ne pas prendre en compte le signe de $q$ si $q<0$</li>\n<li>Utiliser la formule de terme général pour la somme</li>\n</ul>\n</div>\n<div style="background:#f0f9f0; padding:12px; border-radius:4px;">\n<strong>✅ Conseils pratiques :</strong>\n<ul style="margin:8px 0; padding-left:20px;">\n<li>Identifier toujours la raison $q$ et le premier terme $u_0$</li>\n<li>Vérifier si $|q| < 1$ pour une suite convergente</li>\n<li>Utiliser les formules adaptées selon la valeur de $q$</li>\n<li>Faire des vérifications numériques simples</li>\n</ul>\n</div>\n</div>\n\n</div>	easy	\N	24
\.


--
-- Data for Name: cours_coursimage; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.cours_coursimage (id, image, image_type, "position", legende, date_creation, date_modification, cours_id) FROM stdin;
\.


--
-- Data for Name: curriculum_chapitre; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_chapitre (id, est_actif, date_creation, date_modification, titre, ordre, contenu, difficulty, notion_id) FROM stdin;
23	t	2025-09-03 09:36:23.171779+00	2025-09-03 09:36:40.858739+00	Chapitre 2: Suites Arithmétiques	2		medium	19
24	t	2025-09-03 09:37:18.998468+00	2025-09-03 09:37:24.760003+00	Chapitre 3: Suites Géométriques	3		medium	19
27	t	2025-09-03 15:22:21.72489+00	2025-09-03 15:22:21.724923+00	Chapitre 1: Introduction aux Limites et Intuition	1		medium	20
28	t	2025-09-03 15:23:11.931958+00	2025-09-03 15:23:11.931989+00	Chapitre 2: Calcul des Limites	2		medium	20
29	t	2025-09-03 15:24:57.666834+00	2025-09-03 15:24:57.666876+00	Chapitre 3: Asymptotes et Interprétation Graphique	3		medium	20
30	t	2025-09-03 15:25:25.294206+00	2025-09-03 15:25:25.294223+00	Chapitre 4: Les Croissances Comparées	4		medium	20
25	t	2025-09-03 09:38:57.228906+00	2025-09-06 18:31:23.385659+00	Chapitre 4: Variations et Monotonie	4		medium	19
26	t	2025-09-03 09:39:31.043841+00	2025-09-06 18:33:46.035943+00	Chapitre 5: Limites et Convergence	5		medium	19
32	t	2025-09-06 18:37:16.492686+00	2025-09-06 18:37:49.280257+00	Chapitre 6: Suites Définies par Récurrence	6		medium	19
22	t	2025-09-03 09:35:25.744135+00	2025-09-08 05:44:53.542996+00	Chapitre 1: Définitions et Notions de Base	1		medium	19
33	t	2025-09-13 19:44:01.879621+00	2025-09-13 19:44:01.879677+00	Chapitre 1: Définitions et Notions de Base	1		medium	23
34	t	2025-09-13 19:46:57.788056+00	2025-09-13 19:46:57.7881+00	Chapitre 2: Propriétés fondamentales	2		medium	23
35	t	2025-09-13 19:47:38.460881+00	2025-09-13 19:47:38.460925+00	Chapitre 3: Dérivation et variations	3		medium	23
36	t	2025-09-13 19:48:13.525173+00	2025-09-13 19:48:13.52537+00	Chapitre 4: Équations et inéquations logarithmiques	4		medium	23
37	t	2025-09-13 19:49:18.236034+00	2025-09-13 19:49:18.236117+00	Chapitre 5: Étude de fonctions comportant  ln	5		medium	23
38	t	2025-09-13 20:02:45.050116+00	2025-09-13 20:02:45.050222+00	Chapitre 1: Définitions et Notions de Base	1		medium	21
39	t	2025-09-13 20:03:18.757897+00	2025-09-13 20:03:18.757929+00	Chapitre 2: Règles de dérivation usuelles	2		medium	21
41	t	2025-09-13 20:04:46.215416+00	2025-09-13 20:04:46.215499+00	Chapitre 4: Dérivation des quotients et produits	4		medium	21
40	t	2025-09-13 20:03:39.052675+00	2025-09-13 20:05:21.878153+00	Chapitre 3: Dérivation des fonctions composées (règle de la chaîne)	3		medium	21
42	t	2025-09-13 20:05:53.974111+00	2025-09-13 20:05:53.974196+00	Chapitre 5: Signes de la dérivée et variations	5		medium	21
43	t	2025-09-13 20:06:23.258349+00	2025-09-13 20:06:23.258387+00	Chapitre 6: Tangentes et équations locales	6		medium	21
45	t	2025-09-17 12:59:45.278839+00	2025-09-17 12:59:45.278868+00	physiqye test	0		medium	47
46	t	2025-09-17 13:00:52.870268+00	2025-09-17 13:00:52.870295+00	test de chapitre 1: hy	0		medium	47
\.


--
-- Data for Name: curriculum_exercice; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_exercice (id, est_actif, date_creation, date_modification, titre, ordre, contenu, difficulty, question, reponse_correcte, points, chapitre_id, etapes) FROM stdin;
187	t	2025-09-15 13:43:12.162601+00	2025-09-15 13:43:12.162627+00	Exercice 1 — Calculer les premiers termes d'une suite explicite	0	Soit la suite $u_n = 3n + 2$ définie pour $n\\in\\mathbb{N}$.\n**Question 1 :** Calculez les cinq premiers termes de la suite.\n**Question 2 :** Déterminez la différence $u_{n+1}-u_n$ et concluez sur la nature de la suite.	easy	Soit la suite $u_n = 3n + 2$ définie pour $n\\in\\mathbb{N}$.\n**Question 1 :** Calculez les cinq premiers termes de la suite.\n**Question 2 :** Déterminez la différence $u_{n+1}-u_n$ et concluez sur la nature de la suite.	1. $u_0=2,\\;u_1=5,\\;u_2=8,\\;u_3=11,\\;u_4=14$.\n2. $u_{n+1}-u_n=3$, la suite est arithmétique de raison $3$.	1	22	**Question 1 : Calcul des cinq premiers termes**\n● Identifier la formule de la suite : $u_n = 3n + 2$.\n● Remplacer successivement $n$ par $0, 1, 2, 3, 4$ pour obtenir les cinq premiers termes.\n● Pour $n=0$, on a $u_0 = 3×0 + 2 = 2$.\n● Pour $n=1$, on a $u_1 = 3×1 + 2 = 5$.\n● Pour $n=2$, on a $u_2 = 3×2 + 2 = 8$.\n● Pour $n=3$, on a $u_3 = 3×3 + 2 = 11$.\n● Pour $n=4$, on a $u_4 = 3×4 + 2 = 14$.\n● Rassembler les résultats dans une liste ordonnée : $u_0, u_1, u_2, u_3, u_4$.\n**Question 2 : Différence entre termes consécutifs**\n● Écrire la différence $u_{n+1}-u_n$ en remplaçant par l’expression de la suite.\n● Calculer : $u_{n+1} = 3(n+1) + 2 = 3n + 3 + 2 = 3n + 5$.\n● Calculer : $u_n = 3n + 2$.\n● Faire la différence : $(3n+5) - (3n+2) = 3$.\n● Conclure : la différence est constante et vaut $3$, donc la suite est **arithmétique de raison 3**.
188	t	2025-09-15 13:43:12.293425+00	2025-09-15 13:43:12.293442+00	Exercice 2 — Retrouver la formule générale à partir de termes donnés	0	On donne les premiers termes d’une suite :\n$u_1=2,\\;u_2=5,\\;u_3=8,\\;u_4=11$.\n**Question 1 :** Calculez les différences entre termes consécutifs.\n**Question 2 :** En déduisez la nature de la suite et proposez une formule explicite pour $u_n$.	easy	On donne les premiers termes d’une suite :\n$u_1=2,\\;u_2=5,\\;u_3=8,\\;u_4=11$.\n**Question 1 :** Calculez les différences entre termes consécutifs.\n**Question 2 :** En déduisez la nature de la suite et proposez une formule explicite pour $u_n$.	1. Différences : $3,3,3$ donc suite arithmétique de raison $3$.\n2. Avec $u_1= a+b=2$ et $u_2=2a+b=5$, on trouve $a=3,\\;b=-1$. Donc $u_n=3n-1$.	1	22	**Question 1 : Différences entre termes**\n● Identifier les valeurs données : $u_1=2,\\;u_2=5,\\;u_3=8,\\;u_4=11$.\n● Calculer $u_2 - u_1 = 5 - 2 = 3$.\n● Calculer $u_3 - u_2 = 8 - 5 = 3$.\n● Calculer $u_4 - u_3 = 11 - 8 = 3$.\n● Constater que la différence est toujours la même : 3.\n● Conclure : la suite est **arithmétique de raison 3**.\n**Question 2 : Détermination de la formule**\n● Pour une suite arithmétique, la formule générale est de la forme $u_n = an + b$.\n● On utilise les conditions données pour déterminer $a$ et $b$.\n● Avec $u_1=2$, on a $a×1 + b = 2$ donc $a+b=2$.\n● Avec $u_2=5$, on a $a×2 + b = 5$ donc $2a+b=5$.\n● Soustraire les deux équations : $(2a+b) - (a+b) = 5 - 2$.\n● On obtient $a = 3$.\n● Remplacer dans $a+b=2$ : $3 + b = 2$, donc $b=-1$.\n● La formule de la suite est $u_n = 3n - 1$.\n● Vérifier avec $u_3=8$ et $u_4=11$ pour confirmer.
189	t	2025-09-17 12:40:45.476297+00	2025-09-17 12:40:45.476315+00	Exercice 1 — Calculer les premiers termes d'une suite explicite	0	Soit la suite $u_n = 3n + 2$ définie pour $n\\in\\mathbb{N}$.\n**Question 1 :** Calculez les cinq premiers termes de la suite.\n**Question 2 :** Déterminez la différence $u_{n+1}-u_n$ et concluez sur la nature de la suite.	easy	Soit la suite $u_n = 3n + 2$ définie pour $n\\in\\mathbb{N}$.\n**Question 1 :** Calculez les cinq premiers termes de la suite.\n**Question 2 :** Déterminez la différence $u_{n+1}-u_n$ et concluez sur la nature de la suite.	1. $u_0=2,\\;u_1=5,\\;u_2=8,\\;u_3=11,\\;u_4=14$.\n2. $u_{n+1}-u_n=3$, la suite est arithmétique de raison $3$.	1	32	**Question 1 : Calcul des cinq premiers termes**\n● Identifier la formule de la suite : $u_n = 3n + 2$.\n● Remplacer successivement $n$ par $0, 1, 2, 3, 4$ pour obtenir les cinq premiers termes.\n● Pour $n=0$, on a $u_0 = 3×0 + 2 = 2$.\n● Pour $n=1$, on a $u_1 = 3×1 + 2 = 5$.\n● Pour $n=2$, on a $u_2 = 3×2 + 2 = 8$.\n● Pour $n=3$, on a $u_3 = 3×3 + 2 = 11$.\n● Pour $n=4$, on a $u_4 = 3×4 + 2 = 14$.\n● Rassembler les résultats dans une liste ordonnée : $u_0, u_1, u_2, u_3, u_4$.\n**Question 2 : Différence entre termes consécutifs**\n● Écrire la différence $u_{n+1}-u_n$ en remplaçant par l’expression de la suite.\n● Calculer : $u_{n+1} = 3(n+1) + 2 = 3n + 3 + 2 = 3n + 5$.\n● Calculer : $u_n = 3n + 2$.\n● Faire la différence : $(3n+5) - (3n+2) = 3$.\n● Conclure : la différence est constante et vaut $3$, donc la suite est **arithmétique de raison 3**.
190	t	2025-09-17 12:44:01.68845+00	2025-09-17 12:44:01.688477+00	Copiage de texte simple	0	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	easy	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	1. Le chat dort paisiblement sur le canapé.\n2. Phrase copiée correctement.	1	22	Lire attentivement la phrase, identifier chaque mot et respecter les accents, puis réécrire la phrase à l’identique.\n**Question 1 : Copie la phrase donnée**\n● Lis lentement chaque mot.\n● Note la phrase sur ton cahier.\n● Vérifie qu’il n’y a pas d’erreur.\n**Question 2 : Vérifie ton travail**\n● Compare avec la phrase d’origine.\n● Corrige si besoin.
191	t	2025-09-17 12:44:02.246612+00	2025-09-17 12:44:02.246648+00	Copiage avec ponctuation	0	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	easy	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	1. Bonjour ! Comment vas-tu aujourd’hui ?\n2. Signes de ponctuation : !, ?	1	22	Lire la phrase en repérant les signes de ponctuation, copier la phrase avec majuscules et accents, vérifier la position des points d’exclamation et d’interrogation.\n**Question 1 : Copie avec la ponctuation**\n● Lis la phrase complète.\n● Réécris-la avec la ponctuation.\n● Vérifie majuscules et accents.\n**Question 2 : Souligne les signes de ponctuation**\n● Reprends ta copie.\n● Souligne chaque signe (!, ?).
192	t	2025-09-17 12:44:02.89592+00	2025-09-17 12:44:02.895942+00	Copiage d’un court dialogue	0	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	medium	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	1. — Bonjour, dit Paul.\n— Salut ! répondit Marie.\n2. Paul, Marie	1	22	Lire attentivement en observant les tirets, copier le texte avec la même mise en forme, respecter majuscules et accents.\n**Question 1 : Copie le dialogue**\n● Observe les tirets.\n● Écris chaque phrase avec le bon retour à la ligne.\n● Vérifie ton écriture.\n**Question 2 : Mets en évidence les prénoms**\n● Souligne “Paul” et “Marie”.\n● Vérifie que ce sont des majuscules.
193	t	2025-09-17 12:44:03.920998+00	2025-09-17 12:44:03.921022+00	Copiage avec liste	0	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	medium	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	1. ● pomme\n● poire\n● banane\n2. banane, poire, pomme	1	22	Lire chaque mot, copier les mots avec le symbole ●, vérifier l’orthographe des fruits.\n**Question 1 : Recopie la liste**\n● Écris les trois fruits.\n● Mets les symboles ● devant chaque mot.\n● Vérifie ton orthographe.\n**Question 2 : Mets en ordre alphabétique**\n● Compare les mots.\n● Classe-les dans l’ordre A-Z.
194	t	2025-09-17 12:44:04.486634+00	2025-09-17 12:44:04.486661+00	Copiage d’un court texte	0	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	medium	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	1. Il faisait beau hier. Les enfants jouaient au ballon dans le jardin.\n2. Verbes : faisait, jouaient	1	22	Lire attentivement les phrases, identifier la ponctuation, copier sans oublier majuscules et accents.\n**Question 1 : Copie le texte**\n● Lis chaque mot.\n● Copie en deux phrases.\n● Vérifie les majuscules.\n**Question 2 : Souligne les verbes**\n● Relis ta copie.\n● Souligne “faisait” et “jouaient”.
195	t	2025-09-17 12:44:05.020646+00	2025-09-17 12:44:05.020661+00	Copiage avec nombres	0	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	easy	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	1. J’ai 2 chats et 3 chiens.\n2. J’ai deux chats et trois chiens.	1	22	Lire la phrase, identifier les nombres, copier la phrase exactement.\n**Question 1 : Copie la phrase**\n● Écris-la sans changer les chiffres.\n● Vérifie ton orthographe.\n● Relis pour confirmer.\n**Question 2 : Remplace les chiffres par des lettres**\n● Réécris “2” et “3” en lettres.\n● Vérifie les accents.
196	t	2025-09-17 12:44:06.444144+00	2025-09-17 12:44:06.444185+00	Copiage avec majuscules/minuscules	0	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	medium	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	1. Paris est la capitale de la France.\n2. Majuscules : P, F	1	22	Lire la phrase, identifier les majuscules (P, F), copier exactement.\n**Question 1 : Copie la phrase**\n● Reprends le texte.\n● Copie en respectant les majuscules.\n● Vérifie les accents.\n**Question 2 : Souligne les majuscules**\n● Souligne P et F.\n● Vérifie ta copie.
197	t	2025-09-17 12:44:07.154166+00	2025-09-17 12:44:07.154183+00	Copiage avec adjectifs	0	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	medium	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	1. Le petit chien noir court très vite.\n2. Adjectifs : petit, noir	1	22	Lire la phrase, identifier les adjectifs, copier avec exactitude.\n**Question 1 : Copie la phrase**\n● Écris la phrase complète.\n● Vérifie l’orthographe.\n● Relis.\n**Question 2 : Souligne les adjectifs**\n● Identifie “petit” et “noir”.\n● Souligne-les.
198	t	2025-09-17 12:44:07.66764+00	2025-09-17 12:44:07.667665+00	Copiage de phrase interrogative	0	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	easy	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	1. Où habites-tu ?\n2. Verbe : habites	1	22	Lire attentivement la phrase, copier avec accent et point d’interrogation, vérifier l’orthographe.\n**Question 1 : Copie la phrase**\n● Recopie sans erreur.\n● Garde le point d’interrogation.\n● Vérifie ton accent.\n**Question 2 : Mets le verbe en évidence**\n● Souligne “habites”.\n● Vérifie ton travail.
199	t	2025-09-17 12:44:09.053853+00	2025-09-17 12:44:09.053874+00	Copiage d’un texte avec deux phrases	0	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	hard	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	1. Le soleil se couche derrière la montagne. La nuit arrive doucement.\n2. Noms communs : soleil, montagne, nuit	1	22	Lire les deux phrases, copier avec la bonne ponctuation, vérifier les majuscules et accents.\n**Question 1 : Copie les deux phrases**\n● Écris la première phrase.\n● Écris la deuxième phrase.\n● Relis les deux.\n**Question 2 : Souligne les noms communs**\n● Relis le texte.\n● Souligne soleil, montagne, nuit.
200	t	2025-09-17 12:57:10.227119+00	2025-09-17 12:57:10.227151+00	Copiage de texte simple	0	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	easy	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	1. Le chat dort paisiblement sur le canapé.\n2. Phrase copiée correctement.	1	39	Lire attentivement la phrase, identifier chaque mot et respecter les accents, puis réécrire la phrase à l’identique.\n**Question 1 : Copie la phrase donnée**\n● Lis lentement chaque mot.\n● Note la phrase sur ton cahier.\n● Vérifie qu’il n’y a pas d’erreur.\n**Question 2 : Vérifie ton travail**\n● Compare avec la phrase d’origine.\n● Corrige si besoin.
201	t	2025-09-17 12:57:11.227844+00	2025-09-17 12:57:11.227871+00	Copiage avec ponctuation	0	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	easy	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	1. Bonjour ! Comment vas-tu aujourd’hui ?\n2. Signes de ponctuation : !, ?	1	39	Lire la phrase en repérant les signes de ponctuation, copier la phrase avec majuscules et accents, vérifier la position des points d’exclamation et d’interrogation.\n**Question 1 : Copie avec la ponctuation**\n● Lis la phrase complète.\n● Réécris-la avec la ponctuation.\n● Vérifie majuscules et accents.\n**Question 2 : Souligne les signes de ponctuation**\n● Reprends ta copie.\n● Souligne chaque signe (!, ?).
202	t	2025-09-17 12:57:11.955719+00	2025-09-17 12:57:11.955737+00	Copiage d’un court dialogue	0	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	medium	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	1. — Bonjour, dit Paul.\n— Salut ! répondit Marie.\n2. Paul, Marie	1	39	Lire attentivement en observant les tirets, copier le texte avec la même mise en forme, respecter majuscules et accents.\n**Question 1 : Copie le dialogue**\n● Observe les tirets.\n● Écris chaque phrase avec le bon retour à la ligne.\n● Vérifie ton écriture.\n**Question 2 : Mets en évidence les prénoms**\n● Souligne “Paul” et “Marie”.\n● Vérifie que ce sont des majuscules.
203	t	2025-09-17 12:57:13.031078+00	2025-09-17 12:57:13.031091+00	Copiage avec liste	0	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	medium	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	1. ● pomme\n● poire\n● banane\n2. banane, poire, pomme	1	39	Lire chaque mot, copier les mots avec le symbole ●, vérifier l’orthographe des fruits.\n**Question 1 : Recopie la liste**\n● Écris les trois fruits.\n● Mets les symboles ● devant chaque mot.\n● Vérifie ton orthographe.\n**Question 2 : Mets en ordre alphabétique**\n● Compare les mots.\n● Classe-les dans l’ordre A-Z.
204	t	2025-09-17 12:57:14.619081+00	2025-09-17 12:57:14.619107+00	Copiage d’un court texte	0	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	medium	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	1. Il faisait beau hier. Les enfants jouaient au ballon dans le jardin.\n2. Verbes : faisait, jouaient	1	39	Lire attentivement les phrases, identifier la ponctuation, copier sans oublier majuscules et accents.\n**Question 1 : Copie le texte**\n● Lis chaque mot.\n● Copie en deux phrases.\n● Vérifie les majuscules.\n**Question 2 : Souligne les verbes**\n● Relis ta copie.\n● Souligne “faisait” et “jouaient”.
205	t	2025-09-17 12:57:16.219563+00	2025-09-17 12:57:16.219605+00	Copiage avec nombres	0	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	easy	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	1. J’ai 2 chats et 3 chiens.\n2. J’ai deux chats et trois chiens.	1	39	Lire la phrase, identifier les nombres, copier la phrase exactement.\n**Question 1 : Copie la phrase**\n● Écris-la sans changer les chiffres.\n● Vérifie ton orthographe.\n● Relis pour confirmer.\n**Question 2 : Remplace les chiffres par des lettres**\n● Réécris “2” et “3” en lettres.\n● Vérifie les accents.
206	t	2025-09-17 12:57:18.005263+00	2025-09-17 12:57:18.005304+00	Copiage avec majuscules/minuscules	0	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	medium	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	1. Paris est la capitale de la France.\n2. Majuscules : P, F	1	39	Lire la phrase, identifier les majuscules (P, F), copier exactement.\n**Question 1 : Copie la phrase**\n● Reprends le texte.\n● Copie en respectant les majuscules.\n● Vérifie les accents.\n**Question 2 : Souligne les majuscules**\n● Souligne P et F.\n● Vérifie ta copie.
207	t	2025-09-17 12:57:19.662416+00	2025-09-17 12:57:19.66245+00	Copiage avec adjectifs	0	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	medium	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	1. Le petit chien noir court très vite.\n2. Adjectifs : petit, noir	1	39	Lire la phrase, identifier les adjectifs, copier avec exactitude.\n**Question 1 : Copie la phrase**\n● Écris la phrase complète.\n● Vérifie l’orthographe.\n● Relis.\n**Question 2 : Souligne les adjectifs**\n● Identifie “petit” et “noir”.\n● Souligne-les.
208	t	2025-09-17 12:57:20.843007+00	2025-09-17 12:57:20.843028+00	Copiage de phrase interrogative	0	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	easy	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	1. Où habites-tu ?\n2. Verbe : habites	1	39	Lire attentivement la phrase, copier avec accent et point d’interrogation, vérifier l’orthographe.\n**Question 1 : Copie la phrase**\n● Recopie sans erreur.\n● Garde le point d’interrogation.\n● Vérifie ton accent.\n**Question 2 : Mets le verbe en évidence**\n● Souligne “habites”.\n● Vérifie ton travail.
209	t	2025-09-17 12:57:22.850114+00	2025-09-17 12:57:22.850139+00	Copiage d’un texte avec deux phrases	0	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	hard	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	1. Le soleil se couche derrière la montagne. La nuit arrive doucement.\n2. Noms communs : soleil, montagne, nuit	1	39	Lire les deux phrases, copier avec la bonne ponctuation, vérifier les majuscules et accents.\n**Question 1 : Copie les deux phrases**\n● Écris la première phrase.\n● Écris la deuxième phrase.\n● Relis les deux.\n**Question 2 : Souligne les noms communs**\n● Relis le texte.\n● Souligne soleil, montagne, nuit.
210	t	2025-09-17 13:01:36.689984+00	2025-09-17 13:01:36.690014+00	Copiage de texte simple	0	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	easy	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	1. Le chat dort paisiblement sur le canapé.\n2. Phrase copiée correctement.	1	45	Lire attentivement la phrase, identifier chaque mot et respecter les accents, puis réécrire la phrase à l’identique.\n**Question 1 : Copie la phrase donnée**\n● Lis lentement chaque mot.\n● Note la phrase sur ton cahier.\n● Vérifie qu’il n’y a pas d’erreur.\n**Question 2 : Vérifie ton travail**\n● Compare avec la phrase d’origine.\n● Corrige si besoin.
211	t	2025-09-17 13:01:37.231948+00	2025-09-17 13:01:37.231987+00	Copiage avec ponctuation	0	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	easy	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	1. Bonjour ! Comment vas-tu aujourd’hui ?\n2. Signes de ponctuation : !, ?	1	45	Lire la phrase en repérant les signes de ponctuation, copier la phrase avec majuscules et accents, vérifier la position des points d’exclamation et d’interrogation.\n**Question 1 : Copie avec la ponctuation**\n● Lis la phrase complète.\n● Réécris-la avec la ponctuation.\n● Vérifie majuscules et accents.\n**Question 2 : Souligne les signes de ponctuation**\n● Reprends ta copie.\n● Souligne chaque signe (!, ?).
212	t	2025-09-17 13:01:38.090002+00	2025-09-17 13:01:38.090016+00	Copiage d’un court dialogue	0	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	medium	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	1. — Bonjour, dit Paul.\n— Salut ! répondit Marie.\n2. Paul, Marie	1	45	Lire attentivement en observant les tirets, copier le texte avec la même mise en forme, respecter majuscules et accents.\n**Question 1 : Copie le dialogue**\n● Observe les tirets.\n● Écris chaque phrase avec le bon retour à la ligne.\n● Vérifie ton écriture.\n**Question 2 : Mets en évidence les prénoms**\n● Souligne “Paul” et “Marie”.\n● Vérifie que ce sont des majuscules.
213	t	2025-09-17 13:01:38.706202+00	2025-09-17 13:01:38.70624+00	Copiage avec liste	0	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	medium	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	1. ● pomme\n● poire\n● banane\n2. banane, poire, pomme	1	45	Lire chaque mot, copier les mots avec le symbole ●, vérifier l’orthographe des fruits.\n**Question 1 : Recopie la liste**\n● Écris les trois fruits.\n● Mets les symboles ● devant chaque mot.\n● Vérifie ton orthographe.\n**Question 2 : Mets en ordre alphabétique**\n● Compare les mots.\n● Classe-les dans l’ordre A-Z.
214	t	2025-09-17 13:01:39.300483+00	2025-09-17 13:01:39.300508+00	Copiage d’un court texte	0	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	medium	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	1. Il faisait beau hier. Les enfants jouaient au ballon dans le jardin.\n2. Verbes : faisait, jouaient	1	45	Lire attentivement les phrases, identifier la ponctuation, copier sans oublier majuscules et accents.\n**Question 1 : Copie le texte**\n● Lis chaque mot.\n● Copie en deux phrases.\n● Vérifie les majuscules.\n**Question 2 : Souligne les verbes**\n● Relis ta copie.\n● Souligne “faisait” et “jouaient”.
215	t	2025-09-17 13:01:39.872507+00	2025-09-17 13:01:39.872519+00	Copiage avec nombres	0	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	easy	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	1. J’ai 2 chats et 3 chiens.\n2. J’ai deux chats et trois chiens.	1	45	Lire la phrase, identifier les nombres, copier la phrase exactement.\n**Question 1 : Copie la phrase**\n● Écris-la sans changer les chiffres.\n● Vérifie ton orthographe.\n● Relis pour confirmer.\n**Question 2 : Remplace les chiffres par des lettres**\n● Réécris “2” et “3” en lettres.\n● Vérifie les accents.
216	t	2025-09-17 13:01:40.483997+00	2025-09-17 13:01:40.484032+00	Copiage avec majuscules/minuscules	0	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	medium	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	1. Paris est la capitale de la France.\n2. Majuscules : P, F	1	45	Lire la phrase, identifier les majuscules (P, F), copier exactement.\n**Question 1 : Copie la phrase**\n● Reprends le texte.\n● Copie en respectant les majuscules.\n● Vérifie les accents.\n**Question 2 : Souligne les majuscules**\n● Souligne P et F.\n● Vérifie ta copie.
217	t	2025-09-17 13:01:41.208422+00	2025-09-17 13:01:41.208446+00	Copiage avec adjectifs	0	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	medium	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	1. Le petit chien noir court très vite.\n2. Adjectifs : petit, noir	1	45	Lire la phrase, identifier les adjectifs, copier avec exactitude.\n**Question 1 : Copie la phrase**\n● Écris la phrase complète.\n● Vérifie l’orthographe.\n● Relis.\n**Question 2 : Souligne les adjectifs**\n● Identifie “petit” et “noir”.\n● Souligne-les.
218	t	2025-09-17 13:01:41.834029+00	2025-09-17 13:01:41.834054+00	Copiage de phrase interrogative	0	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	easy	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	1. Où habites-tu ?\n2. Verbe : habites	1	45	Lire attentivement la phrase, copier avec accent et point d’interrogation, vérifier l’orthographe.\n**Question 1 : Copie la phrase**\n● Recopie sans erreur.\n● Garde le point d’interrogation.\n● Vérifie ton accent.\n**Question 2 : Mets le verbe en évidence**\n● Souligne “habites”.\n● Vérifie ton travail.
219	t	2025-09-17 13:01:42.487665+00	2025-09-17 13:01:42.4877+00	Copiage d’un texte avec deux phrases	0	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	hard	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	1. Le soleil se couche derrière la montagne. La nuit arrive doucement.\n2. Noms communs : soleil, montagne, nuit	1	45	Lire les deux phrases, copier avec la bonne ponctuation, vérifier les majuscules et accents.\n**Question 1 : Copie les deux phrases**\n● Écris la première phrase.\n● Écris la deuxième phrase.\n● Relis les deux.\n**Question 2 : Souligne les noms communs**\n● Relis le texte.\n● Souligne soleil, montagne, nuit.
220	t	2025-09-17 13:57:04.662593+00	2025-09-17 13:57:04.662603+00	Copiage de texte simple	0	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	easy	Copie attentivement la phrase suivante sans faire de fautes :\n"Le chat dort paisiblement sur le canapé."	1. Le chat dort paisiblement sur le canapé.\n2. Phrase copiée correctement.	1	40	Lire attentivement la phrase, identifier chaque mot et respecter les accents, puis réécrire la phrase à l’identique.\n**Question 1 : Copie la phrase donnée**\n● Lis lentement chaque mot.\n● Note la phrase sur ton cahier.\n● Vérifie qu’il n’y a pas d’erreur.\n**Question 2 : Vérifie ton travail**\n● Compare avec la phrase d’origine.\n● Corrige si besoin.
221	t	2025-09-17 13:57:06.057608+00	2025-09-17 13:57:06.057626+00	Copiage avec ponctuation	0	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	easy	Copie exactement la phrase suivante avec sa ponctuation :\n"Bonjour ! Comment vas-tu aujourd’hui ?"	1. Bonjour ! Comment vas-tu aujourd’hui ?\n2. Signes de ponctuation : !, ?	1	40	Lire la phrase en repérant les signes de ponctuation, copier la phrase avec majuscules et accents, vérifier la position des points d’exclamation et d’interrogation.\n**Question 1 : Copie avec la ponctuation**\n● Lis la phrase complète.\n● Réécris-la avec la ponctuation.\n● Vérifie majuscules et accents.\n**Question 2 : Souligne les signes de ponctuation**\n● Reprends ta copie.\n● Souligne chaque signe (!, ?).
222	t	2025-09-17 13:57:06.650526+00	2025-09-17 13:57:06.650565+00	Copiage d’un court dialogue	0	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	medium	Copie exactement ce petit dialogue :\n— Bonjour, dit Paul.\n— Salut ! répondit Marie.	1. — Bonjour, dit Paul.\n— Salut ! répondit Marie.\n2. Paul, Marie	1	40	Lire attentivement en observant les tirets, copier le texte avec la même mise en forme, respecter majuscules et accents.\n**Question 1 : Copie le dialogue**\n● Observe les tirets.\n● Écris chaque phrase avec le bon retour à la ligne.\n● Vérifie ton écriture.\n**Question 2 : Mets en évidence les prénoms**\n● Souligne “Paul” et “Marie”.\n● Vérifie que ce sont des majuscules.
223	t	2025-09-17 13:57:07.589373+00	2025-09-17 13:57:07.589385+00	Copiage avec liste	0	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	medium	Copie la liste ci-dessous en respectant la mise en forme :\n● pomme\n● poire\n● banane	1. ● pomme\n● poire\n● banane\n2. banane, poire, pomme	1	40	Lire chaque mot, copier les mots avec le symbole ●, vérifier l’orthographe des fruits.\n**Question 1 : Recopie la liste**\n● Écris les trois fruits.\n● Mets les symboles ● devant chaque mot.\n● Vérifie ton orthographe.\n**Question 2 : Mets en ordre alphabétique**\n● Compare les mots.\n● Classe-les dans l’ordre A-Z.
224	t	2025-09-17 13:57:08.145586+00	2025-09-17 13:57:08.145602+00	Copiage d’un court texte	0	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	medium	Copie exactement le texte suivant :\n"Il faisait beau hier. Les enfants jouaient au ballon dans le jardin."	1. Il faisait beau hier. Les enfants jouaient au ballon dans le jardin.\n2. Verbes : faisait, jouaient	1	40	Lire attentivement les phrases, identifier la ponctuation, copier sans oublier majuscules et accents.\n**Question 1 : Copie le texte**\n● Lis chaque mot.\n● Copie en deux phrases.\n● Vérifie les majuscules.\n**Question 2 : Souligne les verbes**\n● Relis ta copie.\n● Souligne “faisait” et “jouaient”.
225	t	2025-09-17 13:57:08.691708+00	2025-09-17 13:57:08.691731+00	Copiage avec nombres	0	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	easy	Copie la phrase suivante en respectant les nombres :\n"J’ai 2 chats et 3 chiens."	1. J’ai 2 chats et 3 chiens.\n2. J’ai deux chats et trois chiens.	1	40	Lire la phrase, identifier les nombres, copier la phrase exactement.\n**Question 1 : Copie la phrase**\n● Écris-la sans changer les chiffres.\n● Vérifie ton orthographe.\n● Relis pour confirmer.\n**Question 2 : Remplace les chiffres par des lettres**\n● Réécris “2” et “3” en lettres.\n● Vérifie les accents.
226	t	2025-09-17 13:57:09.276735+00	2025-09-17 13:57:09.27675+00	Copiage avec majuscules/minuscules	0	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	medium	Copie exactement la phrase suivante en respectant majuscules et minuscules :\n"Paris est la capitale de la France."	1. Paris est la capitale de la France.\n2. Majuscules : P, F	1	40	Lire la phrase, identifier les majuscules (P, F), copier exactement.\n**Question 1 : Copie la phrase**\n● Reprends le texte.\n● Copie en respectant les majuscules.\n● Vérifie les accents.\n**Question 2 : Souligne les majuscules**\n● Souligne P et F.\n● Vérifie ta copie.
227	t	2025-09-17 13:57:10.114014+00	2025-09-17 13:57:10.114025+00	Copiage avec adjectifs	0	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	medium	Copie la phrase suivante en respectant les adjectifs :\n"Le petit chien noir court très vite."	1. Le petit chien noir court très vite.\n2. Adjectifs : petit, noir	1	40	Lire la phrase, identifier les adjectifs, copier avec exactitude.\n**Question 1 : Copie la phrase**\n● Écris la phrase complète.\n● Vérifie l’orthographe.\n● Relis.\n**Question 2 : Souligne les adjectifs**\n● Identifie “petit” et “noir”.\n● Souligne-les.
228	t	2025-09-17 13:57:11.970441+00	2025-09-17 13:57:11.970454+00	Copiage de phrase interrogative	0	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	easy	Copie la phrase suivante en gardant le point d’interrogation :\n"Où habites-tu ?"	1. Où habites-tu ?\n2. Verbe : habites	1	40	Lire attentivement la phrase, copier avec accent et point d’interrogation, vérifier l’orthographe.\n**Question 1 : Copie la phrase**\n● Recopie sans erreur.\n● Garde le point d’interrogation.\n● Vérifie ton accent.\n**Question 2 : Mets le verbe en évidence**\n● Souligne “habites”.\n● Vérifie ton travail.
229	t	2025-09-17 13:57:12.672425+00	2025-09-17 13:57:12.672437+00	Copiage d’un texte avec deux phrases	0	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	hard	Copie le texte suivant sans oublier la ponctuation :\n"Le soleil se couche derrière la montagne. La nuit arrive doucement."	1. Le soleil se couche derrière la montagne. La nuit arrive doucement.\n2. Noms communs : soleil, montagne, nuit	1	40	Lire les deux phrases, copier avec la bonne ponctuation, vérifier les majuscules et accents.\n**Question 1 : Copie les deux phrases**\n● Écris la première phrase.\n● Écris la deuxième phrase.\n● Relis les deux.\n**Question 2 : Souligne les noms communs**\n● Relis le texte.\n● Souligne soleil, montagne, nuit.
\.


--
-- Data for Name: curriculum_exerciceimage; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_exerciceimage (id, image, image_type, "position", legende, date_creation, date_modification, exercice_id) FROM stdin;
\.


--
-- Data for Name: curriculum_matiere; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_matiere (id, est_actif, date_creation, date_modification, titre, ordre, description, couleur, svg_icon) FROM stdin;
9	t	2025-08-10 12:38:08.514591+00	2025-09-12 15:05:49.817271+00	Chimie	5	Découvrez les secrets de la matière	#9C27B0	<svg id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 500 500" data-imageid="scientist-72" imageName="Scientist" class="illustrations_image" style="width: 175px;"><defs><style>.cls-1_scientist-72{fill:url(#linear-gradient);}.cls-1_scientist-72,.cls-2_scientist-72,.cls-3_scientist-72,.cls-4_scientist-72,.cls-5_scientist-72,.cls-6_scientist-72,.cls-7_scientist-72,.cls-8_scientist-72,.cls-9_scientist-72,.cls-10_scientist-72,.cls-11_scientist-72,.cls-12_scientist-72,.cls-13_scientist-72,.cls-14_scientist-72,.cls-15_scientist-72,.cls-16_scientist-72,.cls-17_scientist-72,.cls-18_scientist-72,.cls-19_scientist-72,.cls-20_scientist-72,.cls-21_scientist-72,.cls-22_scientist-72,.cls-23_scientist-72,.cls-24_scientist-72,.cls-25_scientist-72,.cls-26_scientist-72,.cls-27_scientist-72,.cls-28_scientist-72,.cls-29_scientist-72,.cls-30_scientist-72,.cls-31_scientist-72,.cls-32_scientist-72,.cls-33_scientist-72,.cls-34_scientist-72,.cls-35_scientist-72{stroke-width:0px;}.cls-2_scientist-72{fill:url(#linear-gradient-22-scientist-72);}.cls-2_scientist-72,.cls-3_scientist-72{opacity:.17;}.cls-2_scientist-72,.cls-3_scientist-72,.cls-23_scientist-72,.cls-35_scientist-72{isolation:isolate;}.cls-3_scientist-72{fill:url(#linear-gradient-19-scientist-72);}.cls-4_scientist-72{fill:url(#linear-gradient-29-scientist-72);}.cls-5_scientist-72{fill:url(#linear-gradient-30-scientist-72);}.cls-6_scientist-72{fill:url(#linear-gradient-28-scientist-72);}.cls-7_scientist-72{fill:url(#linear-gradient-25-scientist-72);}.cls-8_scientist-72{fill:url(#linear-gradient-11-scientist-72);}.cls-9_scientist-72{fill:url(#linear-gradient-12-scientist-72);}.cls-10_scientist-72{fill:url(#linear-gradient-13-scientist-72);}.cls-11_scientist-72{fill:url(#linear-gradient-10-scientist-72);}.cls-12_scientist-72{fill:url(#linear-gradient-17-scientist-72);}.cls-13_scientist-72{fill:url(#linear-gradient-16-scientist-72);}.cls-14_scientist-72{fill:url(#linear-gradient-15-scientist-72);}.cls-15_scientist-72{fill:url(#linear-gradient-23-scientist-72);}.cls-16_scientist-72{fill:url(#linear-gradient-21-scientist-72);}.cls-17_scientist-72{fill:url(#linear-gradient-18-scientist-72);}.cls-18_scientist-72{fill:url(#linear-gradient-14-scientist-72);}.cls-19_scientist-72{fill:url(#linear-gradient-20-scientist-72);}.cls-20_scientist-72{fill:url(#linear-gradient-27-scientist-72);}.cls-21_scientist-72{fill:url(#linear-gradient-24-scientist-72);}.cls-22_scientist-72{fill:url(#linear-gradient-26-scientist-72);}.cls-23_scientist-72{opacity:.42;}.cls-23_scientist-72,.cls-34_scientist-72,.cls-35_scientist-72{fill:#68e1fd;}.cls-24_scientist-72{fill:url(#linear-gradient-4-scientist-72);}.cls-25_scientist-72{fill:url(#linear-gradient-2-scientist-72);}.cls-26_scientist-72{fill:url(#linear-gradient-3-scientist-72);}.cls-27_scientist-72{fill:url(#linear-gradient-8-scientist-72);}.cls-28_scientist-72{fill:url(#linear-gradient-9-scientist-72);}.cls-29_scientist-72{fill:url(#linear-gradient-7-scientist-72);}.cls-30_scientist-72{fill:url(#linear-gradient-5-scientist-72);}.cls-31_scientist-72{fill:url(#linear-gradient-6-scientist-72);}.cls-32_scientist-72{fill:#231f20;}.cls-33_scientist-72{fill:#ffb4a3;}.cls-35_scientist-72{opacity:.25;}</style><linearGradient id="linear-gradient-scientist-72" x1="-2403.36" y1="-5304.18" x2="-2402.89" y2="-5136.13" gradientTransform="translate(2502.67 5466.3)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".97" stop-color="#fff"/></linearGradient><linearGradient id="linear-gradient-2-scientist-72" x1="-2403.53" y1="-5205.79" x2="-2397.14" y2="-4883.41" gradientTransform="translate(2502.67 5466.3)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".97" stop-color="#000"/></linearGradient><linearGradient id="linear-gradient-3-scientist-72" x1="-2405.31" y1="-5163.97" x2="-2430.16" y2="-5163.73" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-4-scientist-72" x1="-2403.44" y1="-5249.46" x2="-2403.75" y2="-5265.55" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-5-scientist-72" x1="-2269.33" y1="-5393.94" x2="-2261.43" y2="-5367.75" gradientTransform="translate(2503.04 5523.3)" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-6-scientist-72" x1="-2268.12" y1="-5375.63" x2="-2267.17" y2="-5394.81" gradientTransform="translate(2503.04 5523.3)" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-7-scientist-72" x1="-2265.71" y1="-5190.95" x2="-2364.41" y2="-5243.5" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-8-scientist-72" x1="-2245.11" y1="-5267.56" x2="-2198.95" y2="-5517.5" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-9-scientist-72" x1="-2710.82" y1="-5184.39" x2="-1578.98" y2="-5209.95" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-10-scientist-72" x1="-2255.5" y1="-5135.1" x2="-2396.33" y2="-5398.06" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-11-scientist-72" x1="-2278.14" y1="-5144.81" x2="-1988.43" y2="-4950.26" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-12-scientist-72" x1="-2315.53" y1="-5283.5" x2="-2247.37" y2="-5009.43" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-13-scientist-72" x1="-2346.72" y1="-5240.87" x2="-2306.01" y2="-5113.06" gradientTransform="translate(2503.04 5523.3)" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-14-scientist-72" x1="-2123.77" y1="-5136.99" x2="-2097.26" y2="-5132.89" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-15-scientist-72" x1="-2119.84" y1="-5126.01" x2="-2097.47" y2="-5126.01" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-16-scientist-72" x1="-2098.63" y1="-5133.88" x2="-2065.74" y2="-5137.47" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-17-scientist-72" x1="-2138.43" y1="-5230.79" x2="-2138.59" y2="-5250.19" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-18-scientist-72" x1="-2161.26" y1="-5247.85" x2="-2193.81" y2="-5237.91" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-19-scientist-72" x1="-2137.21" y1="-5239.18" x2="-2058.78" y2="-5190.42" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-20-scientist-72" x1="-2091.94" y1="-5212.88" x2="-2065.47" y2="-5214.81" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-21-scientist-72" x1="-2125.97" y1="-5220.77" x2="-2094.83" y2="-5219.1" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-22-scientist-72" x1="-2123.65" y1="-5141.18" x2="-2050.59" y2="-5295.66" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-23-scientist-72" x1="-2115.42" y1="-5297.17" x2="-2108.4" y2="-5297.17" gradientTransform="translate(2503.04 5523.3)" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-24-scientist-72" x1="-2084.16" y1="-5226.72" x2="-2072.56" y2="-5230.51" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-25-scientist-72" x1="-2105.24" y1="-5243.01" x2="-2091.35" y2="-5239.2" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-26-scientist-72" x1="-2098.55" y1="-5261.26" x2="-2086.59" y2="-5261.26" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-27-scientist-72" x1="-2115.64" y1="-5258.17" x2="-2106.02" y2="-5258.17" xlink:href="#linear-gradient-scientist-72"/><linearGradient id="linear-gradient-28-scientist-72" x1="-2084.7" y1="-5129.1" x2="-2071.26" y2="-5129.1" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-29-scientist-72" x1="-2168.83" y1="-5245.99" x2="-2168.73" y2="-5245.99" xlink:href="#linear-gradient-2-scientist-72"/><linearGradient id="linear-gradient-30-scientist-72" x1="-2065.56" y1="-5211.07" x2="-2102.49" y2="-5214.62" xlink:href="#linear-gradient-scientist-72"/></defs><g id="background_scientist-72"><path class="cls-35_scientist-72 targetColor" d="M463.93,273.73c-2.04,21.02,1.79,70.4-35.06,103.29-24.55,21.91-67.17,36.48-141.6,30.47-186.16-15.03-202.94,26.38-227.22-66.3,0,0-.95-40.02-11.37-49.96-10.42-9.94-12.92-42.72-12.92-42.72,0,0-3.27-46.92,46.49-72.4,49.76-25.47,75.31,13.21,98.98,5.7,23.67-7.51,10.75-43.49,55.56-60.53,44.81-17.04,67.14-10.42,88.64,0,21.49,10.42,57.45,17.58,78.29,6.89,20.84-10.68,53.8,4.35,47.76,41.19-6.04,36.84,15.86,69.34,12.45,104.36h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-35_scientist-72 targetColor" d="M463.93,273.73c-2.04,21.02,1.79,70.4-35.06,103.29-18.4,16.43-46.97,28.72-91.47,31.33-16.71.88-33.46.6-50.13-.84-174.2-14.06-200.07,21.28-222.59-50.04-1.53-4.88-3.07-10.31-4.63-16.27,0,0-.95-40.02-11.37-49.96-10.42-9.94-12.92-42.72-12.92-42.72,0,0-3.27-46.92,46.49-72.4,49.76-25.47,75.31,13.21,98.98,5.7,23.67-7.51,10.75-43.49,55.56-60.53,44.81-17.04,67.14-10.42,88.64,0,21.49,10.42,57.45,17.58,78.29,6.89,20.84-10.68,53.8,4.35,47.76,41.19-6.04,36.84,15.86,69.34,12.45,104.36h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-23_scientist-72 targetColor" d="M346.56,362.68c-.4,17.05-4.51,32.94-9.16,45.64-16.71.88-33.46.6-50.13-.84-174.2-14.06-200.07,21.28-222.59-50.04l34.47-43.02s123.64-92.47,268.38-79.36c144.74,13.11-20.02,86.95-20.97,127.62Z" style="fill: rgb(104, 225, 253);"/><circle class="cls-35_scientist-72 targetColor" cx="200.32" cy="103.78" r="12.63" style="fill: rgb(104, 225, 253);"/><circle class="cls-35_scientist-72 targetColor" cx="121.8" cy="149.25" r="9.47" style="fill: rgb(104, 225, 253);"/></g><g id="flask_1_scientist-72"><path class="cls-34_scientist-72 targetColor" d="M125.21,211.75v163.92c0,14.1-11.43,25.53-25.53,25.53s-25.53-11.43-25.53-25.53h0v-163.93h51.06,0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-1_scientist-72" d="M125.21,211.75v163.92c0,14.1-11.43,25.53-25.53,25.53s-25.53-11.43-25.53-25.53h0v-163.93h51.06,0Z"/><path class="cls-34_scientist-72 targetColor" d="M118.57,256.36v117.38c0,10-7.83,18.44-17.82,18.72-10.13.28-18.56-7.7-18.85-17.82v-118.27l5.63,3.51c9.57,5.98,21.96,4.83,30.26-2.82l.78-.7h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-25_scientist-72" d="M118.57,256.36v117.38c0,10-7.83,18.44-17.82,18.72-10.13.28-18.56-7.7-18.85-17.82v-118.27l5.63,3.51c9.57,5.98,21.96,4.83,30.26-2.82l.78-.7h0Z"/><path class="cls-26_scientist-72" d="M121.8,207.64v163.96c0,14.1-9.89,25.54-22.13,25.54s-22.13-11.43-22.13-25.53v-163.92l44.25-.05h0Z"/><path class="cls-34_scientist-72 targetColor" d="M134.34,204.54c0,3.98-3.22,7.21-7.2,7.21h-56.02c-3.99.14-7.33-2.98-7.46-6.97-.14-3.99,2.98-7.33,6.97-7.46h56.49c3.98,0,7.21,3.23,7.21,7.21h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-24_scientist-72" d="M134.34,204.54c0,3.98-3.22,7.21-7.2,7.21h-56.02c-3.99.14-7.33-2.98-7.46-6.97-.14-3.99,2.98-7.33,6.97-7.46h56.49c3.98,0,7.21,3.23,7.21,7.21h0Z"/></g><g id="flask_2_scientist-72"><path class="cls-34_scientist-72 targetColor" d="M207.54,128.19h55.99c3.99,0,7.22,3.23,7.22,7.22h0c0,3.99-3.23,7.22-7.22,7.22h-55.99c-3.99,0-7.22-3.23-7.22-7.22h0c0-3.99,3.23-7.22,7.22-7.22Z" style="fill: rgb(104, 225, 253);"/><path class="cls-30_scientist-72" d="M207.54,128.19h55.99c3.99,0,7.22,3.23,7.22,7.22h0c0,3.99-3.23,7.22-7.22,7.22h-55.99c-3.99,0-7.22-3.23-7.22-7.22h0c0-3.99,3.23-7.22,7.22-7.22Z"/><path class="cls-31_scientist-72" d="M207.54,128.19h55.99c3.99,0,7.22,3.23,7.22,7.22h0c0,3.99-3.23,7.22-7.22,7.22h-55.99c-3.99,0-7.22-3.23-7.22-7.22h0c0-3.99,3.23-7.22,7.22-7.22Z"/><path class="cls-34_scientist-72 targetColor" d="M325.07,317.95c0,49.45-40.08,89.54-89.53,89.54h-.64c-49.43-.35-89.49-41.23-88.88-90.65.43-34.78,20.95-66.16,52.65-80.49,7.89-3.57,12.97-11.42,12.97-20.08v-73.65h47.86v73.66c0,8.67,5.08,16.53,12.98,20.1,32.03,14.51,52.6,46.41,52.6,81.57h-.01Z" style="fill: rgb(104, 225, 253);"/><path class="cls-29_scientist-72" d="M325.07,317.95c0,49.45-40.08,89.54-89.53,89.54h-.64c-49.43-.35-89.49-41.23-88.88-90.65.43-34.78,20.95-66.16,52.65-80.49,7.89-3.57,12.97-11.42,12.97-20.08v-73.65h47.86v73.66c0,8.67,5.08,16.53,12.98,20.1,32.03,14.51,52.6,46.41,52.6,81.57h-.01Z"/><path class="cls-27_scientist-72" d="M325.07,317.95c0,49.45-40.08,89.54-89.53,89.54h-.64c-49.43-.35-89.49-41.23-88.88-90.65.43-34.78,20.95-66.16,52.65-80.49,7.89-3.57,12.97-11.42,12.97-20.08v-73.65h47.86v73.66c0,8.67,5.08,16.53,12.98,20.1,32.03,14.51,52.6,46.41,52.6,81.57h-.01Z"/><path class="cls-28_scientist-72" d="M319.83,318.12c0,46.06-37.34,83.4-83.4,83.4h-.6c-46.04-.33-83.35-38.41-82.79-84.44.4-32.39,19.52-61.62,49.04-74.97,7.35-3.36,15.55-10.63,15.55-18.7v-80.78h35.89v80.8c0,8.09,9.96,15.38,17.32,18.72,29.82,13.52,48.98,43.23,48.98,75.98h0Z"/><path class="cls-34_scientist-72 targetColor" d="M188.14,316.95s-8.07-5.68-27.07-2.21c0,0-1.97-11.65,15.7-13.4s56.13,4.88,72.72-5.22,45.83-17.65,58.99,5.22c0,0-29.14,4.2-42.08,15.61-12.94,11.41-56.79,12.65-78.26,0h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-11_scientist-72" d="M188.14,316.95s-8.07-5.68-27.07-2.21c0,0-1.97-11.65,15.7-13.4s56.13,4.88,72.72-5.22,45.83-17.65,58.99,5.22c0,0-29.14,4.2-42.08,15.61-12.94,11.41-56.79,12.65-78.26,0h0Z"/><path class="cls-34_scientist-72 targetColor" d="M311.8,317.95c.44,41.62-32.95,75.72-74.57,76.16s-75.72-32.95-76.16-74.57v-1.59c0-41.62,50.44,25.09,79.09-5.09,27.19-28.63,71.64-36.53,71.64,5.09Z" style="fill: rgb(104, 225, 253);"/><path class="cls-8_scientist-72" d="M311.8,317.95c.44,41.62-32.95,75.72-74.57,76.16s-75.72-32.95-76.16-74.57v-1.59c0-41.62,50.44,25.09,79.09-5.09,27.19-28.63,71.64-36.53,71.64,5.09Z"/><path class="cls-9_scientist-72" d="M235.54,148.68v83.52c0,.68-.11,1.35-.34,1.98-1.16,3.3-6.36,11.82-17.4,17.98-26.19,14.61-34.73,51.19-35.68,52.28-3.28,3.77-11.21,10.7-19.86,2.06-11.37-11.32,12.89-44.21,20.65-52.31,10.93-11.4,33.94-14.55,34.26-25.28.26-8.88.09-62.06,0-80.21,0-3.34,2.68-6.06,6.02-6.07h6.26c3.34-.02,6.07,2.68,6.09,6.02v.03h0Z"/><circle class="cls-10_scientist-72" cx="172.85" cy="334.31" r="13.57"/></g><g id="charcater_scientist-72"><path class="cls-32_scientist-72" d="M424.01,387.31s-4.31,8.68-4.08,10.62c.24,1.94,4.27,2.32,8.17,0,3.9-2.32,6.84-8.72,6.84-8.72l.97,4.2h1.89l-2.86-10.48s-8.04,3.28-10.94,4.38h0Z"/><path class="cls-32_scientist-72" d="M386.23,384.15c.51,1.06.79,2.22.8,3.4-.12,1.54-.8,6.99-.8,6.99h-1.56v-3.08s-4.5,4.38-7.1,4.97-8.88,2.52-10.65.84,8-9.75,8-9.75l11.31-3.37Z"/><path class="cls-33_scientist-72" d="M376.14,386.37c-1.05.97-2.61,2.14-2,3.42.32.54.87.92,1.49,1.02,1.83.43,3.73-.21,5.5-.84,1.05-.31,2.04-.8,2.93-1.44,1.26-1.12,2.04-2.69,2.18-4.38.19-1.68.71-5.43.49-7.09-.47-3.31-3.58-8.1-5.88-3.99-1.82,3.38-1.55,10.42-4.69,13.3h-.02Z"/><path class="cls-33_scientist-72" d="M425,374.09c.24-.1.52.01.62.25,0,.01.01.03.01.04l-1.01.06c-1.04,1.38-.16,3.3,0,5.04.61,5.5-2.93,11.77-2.65,12.07.72.35,1.48.61,2.27.76,3.5.92,8.21-4.93,10.09-8.01.28-.4.46-.86.53-1.35-.01-.6-.19-1.18-.5-1.68l-2.08-4.12c-.99-1.95-2.46-4.2-4.65-4.07-1.67.12-1.67-.49-2.62.99v.02Z"/><path class="cls-34_scientist-72 targetColor" d="M377.29,315.92c-1.78,5.62-2.84,11.45-3.16,17.33-.23,6.34.8,12.61,1.82,18.74l2.52,15.17c.56,3.36-.66,7.44.89,9.96,1.55,2.52,6.17,3.02,7.8.64-.18-11.46-.42-18.39.46-29.77.63-8.12,3.36-17.39,7.04-23.14,2.52-3.9,11.63-18.91,14.09-22.87,2.45-3.96,2.05-5.75,1.45-11.22-1.19-10.7-16.17-7.52-21.23-2.21-5.26,5.5-9.12,18.64-11.68,27.36h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-18_scientist-72" d="M408.73,301.98c-.72,1.17-2.02,3.28-3.55,5.78-3.7,6.03-8.78,14.29-10.54,17.08-3.67,5.75-6.41,15.02-7.04,23.14-.88,11.37-.65,18.31-.46,29.77-.59.8-1.47,1.33-2.45,1.46-.61.1-1.23.1-1.83,0h-.04c-1.4-.17-2.67-.93-3.47-2.09-1.55-2.52-.33-6.57-.89-9.96-.84-5.04-1.68-10.1-2.52-15.17-1.02-6.14-2.04-12.4-1.82-18.74.32-5.88,1.39-11.71,3.16-17.33,2.52-8.71,6.41-21.86,11.66-27.37,5.04-5.3,20.04-8.49,21.23,2.21.62,5.5,1.01,7.25-1.43,11.21h-.01Z"/><path class="cls-14_scientist-72" d="M405.19,307.77c-3.7,6.03-8.78,14.29-10.54,17.08-3.67,5.75-6.41,15.02-7.04,23.14-.88,11.37-.65,18.31-.46,29.77-.59.8-1.47,1.33-2.45,1.46h-1.87v-40.65c0-13.26,14.57-36.15,14.57-36.15,2.86-3.08,5.8,1.1,7.8,5.35h0Z"/><path class="cls-34_scientist-72 targetColor" d="M416.07,360.77c2.05,5.53,3.82,11.37,7.12,15.06,2.12,2.37,2.66,3.48,7.41-2.03,2.31-2.68.42-5.69-.74-9.29-5.72-17.8-3.04-39.09-2.93-59.08.09-16.06-26.72-28.81-27.79-14.76-2.87,37.49,11.47,55.33,16.94,70.11h-.01Z" style="fill: rgb(104, 225, 253);"/><path class="cls-13_scientist-72" d="M430.03,374.44c-2.56,2.43-3.95,4.67-6.07,2.3-3.3-3.69-5.83-10.46-7.89-15.97-5.47-14.78-18.69-34.35-16.94-70.11.61-12.61,22.51-3.67,26.99,9.88.53,1.57.8,3.22.8,4.88-.11,19.99-2.79,41.27,2.93,59.08,1.16,3.59,2.75,7.52.17,9.94h.01Z"/><path class="cls-32_scientist-72" d="M385.47,147.79c5.76.25,10.86,3.67,15.3,7.34.67.62,1.43,1.13,2.26,1.52,1.06.42,1.27.89,2.4,1.03,4.2.56,8.72,3.17,10.72,6.9s2.67,8.04,2.98,12.26c.27,3.85.35,7.99,2.63,11.1,3.53,4.82,10.56,5.04,15.72,8.05,3.79,2.26,6.54,5.93,7.65,10.21.91,3.48.74,7.14,1.21,10.7s1.8,7.3,4.79,9.25c-5.72-.08-13.97,4.29-19.7,4.2-2.05,0-1.62-4.51-3.59-5.04-2.07-.67-4.01-1.69-5.72-3.03-8.17-5.93-14.33-14.21-17.65-23.75-1.29-3.76-14.68,15.22-16.24,11.57-8.41-19.71,7.57-29.56,3.64-30.37-3.24-.68-6.6.4-9.92.24-19.38-.92-15.25-33,3.54-32.18h-.02Z"/><path class="cls-34_scientist-72 targetColor" d="M362.78,219.57c-4.15,0-8.25-.84-12.31-1.74l-14.4-3.11c-.68-.2-1.39-.24-2.08-.1-.77.3-1.41.87-1.79,1.61-2.44,4.09-.45,9.68,3.2,12.73,3.66,3.05,8.5,4.2,13.17,5.11,6.24,1.24,12.69,2.29,18.92.99,7.69-1.61,18.54-3.84,24.56-8.88.79-.66-2.76-4.09-2.29-4.99.44-1.06.64-2.21.59-3.36.05-2.45,8.83-19.07,6.14-20.37-2.52-1.24-12.45,12.84-14.12,14.37-5.35,4.91-12.33,7.66-19.59,7.75h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-12_scientist-72" d="M391.18,223.97c.67.98,1.25,1.89.84,2.19-6.03,5.04-16.87,7.27-24.56,8.88-6.23,1.29-12.69.24-18.92-.99-4.67-.92-9.52-2.05-13.17-5.11-.66-.55-1.26-1.17-1.78-1.85-.02-.03-.04-.05-.06-.08-2.4-3.14-3.36-7.46-1.36-10.79.38-.74,1.02-1.31,1.79-1.61.69-.14,1.41-.1,2.08.1l14.4,3.1c4.05.84,8.15,1.76,12.31,1.74,7.26-.09,14.23-2.85,19.59-7.75,1.68-1.53,11.57-15.6,14.12-14.37,2.69,1.3-6.09,17.92-6.14,20.37.06,1.15-.14,2.3-.59,3.36-.24.48.64,1.68,1.4,2.78l.05.03h0Z"/><path class="cls-17_scientist-72" d="M332.2,216.24s.84-1.82,1.79-1.61,3.68,8.5-.43,12.4c0,0-3.23-6.79-1.36-10.79h0Z"/><path class="cls-3_scientist-72" d="M392.06,226.19c-6.03,5.04-16.87,7.27-24.56,8.88-6.23,1.29-12.69.24-18.92-.99-4.67-.92-9.52-2.05-13.17-5.11-.66-.55-1.26-1.17-1.78-1.85-.02-.03-.04-.05-.06-.08l.37-6.62c.48.43,3.06,1.68,14.64,5.14,16.92,5.09,37.99-6.04,37.99-6.04l4.62,4.46h0c.66.99,1.26,1.91.89,2.21h-.02Z"/><path class="cls-34_scientist-72 targetColor" d="M437.94,299.52c-.05.91-.45,1.78-1.12,2.4-.76.44-1.66.59-2.52.43-2.35-.18-5.04-.29-7.79-.59-2.9-.27-5.76-.88-8.52-1.82-9.67-3.45-18.57-9.61-21.78-10.93-2.3-.92-11.63,1.5-13.37-.28-4.12-4.2,3.4-10.7,4.69-16.46,2.24-10.09,7.07-20.18,4.93-30.26-.68-2.69-1.52-5.34-2.52-7.93-2.08-6.16-4.63-14.77-2.68-21.23,1.52-5.04,3.96-12.32,8.12-15.75,4.79-3.95,6.46-2.13,12.67-1.96,4.33.12,16.16,4.92,17.46,6.78,13.53,19.52,10.61,56.97,12.74,85.37.39,4.07.29,8.18-.3,12.22h-.01Z" style="fill: rgb(104, 225, 253);"/><path class="cls-19_scientist-72" d="M437.94,299.52c-.05.91-.45,1.77-1.11,2.4-.71.53-3.71-4.2-4.59-4.3-5.49-.41-8.9,3.51-14.29,2.33-.48-1.13-.16-2.24,1.32-3.36,7.65-5.56,4.89-62.52,2.87-78.03,4.64,1.6,2.52-17.78,3.31-16.6,13.53,19.51,10.61,56.95,12.74,85.36.41,4.06.32,8.16-.26,12.21h.01Z"/><path class="cls-16_scientist-72" d="M419.28,296.62c-1.48,1.08-1.8,2.2-1.32,3.36-7.37-1.62-14.87-7.87-21.78-10.93-2.28-.99-11.63,1.5-13.37-.28-4.12-4.2,3.4-10.7,4.69-16.46,2.24-10.09,7.07-20.18,4.93-30.26-.69-2.69-1.53-5.33-2.52-7.92-2.08-6.16-4.63-14.77-2.69-21.23,1.53-5.04,3.97-12.32,8.13-15.75,4.79-3.95,6.46-2.13,12.67-1.96,1.61,0,14.69,5.83,17.46,6.78,2.01,15.53,1.45,89.09-6.2,94.65Z"/><path class="cls-2_scientist-72" d="M393.43,237.24s2.52,11.62.41,19.19-7.75,31.68-7.76,32.34c0,.66,3.67,1.03,3.67,1.03l19.65-13.85,6,5.88s12.7-8.8,21.66-22.03l-.29-7.69-42.12,22.9c.95-2.05,1.52-4.26,1.68-6.51.41-4.03,2.8-23.01-2.89-31.26h0Z"/><polygon class="cls-34_scientist-72 targetColor" points="390.55 215.02 387.62 220.2 393.43 237.24 394.64 236.86 393.99 218.99 390.55 215.02" style="fill: rgb(104, 225, 253);"/><polygon class="cls-15_scientist-72" points="390.55 215.02 387.62 220.2 393.43 237.24 394.64 236.86 393.99 218.99 390.55 215.02"/><path class="cls-32_scientist-72" d="M394.01,215.67c-.13,6.73-.45,18.4.36,17.4,2.89-3.56,17.09-37.74,12.44-38.43-5.59-.84-12.35-2.39-12.8,21.03Z"/><path class="cls-33_scientist-72" d="M406.78,195.46s-4.56,6.21-8.29,8.63c-.56.36-1.31.2-1.67-.36-.15-.24-.22-.52-.18-.8.18-1.34.18-2.69,0-4.03-.13-1.02-.52-1.99-1.13-2.82-.3-.38-.67-.69-1.08-.92-3.81-2.13,4.2-18.23,7.9-13.63l4.46,13.92h0Z"/><path class="cls-32_scientist-72" d="M368.19,165.91c-1.46,4.51-.56,10.26,3.51,12.68,2.16,1.29,4.93,1.5,6.73,3.23,3.09-3.87,9.64-3.58,12.44-7.65,1.17-1.85,1.51-4.1.93-6.2-.58-2.08-1.65-3.99-3.12-5.58-1.8-2.18-4.15-3.84-6.81-4.82-6.79-2.28-11.58,1.92-13.68,8.35h0Z"/><path class="cls-33_scientist-72" d="M375.21,171.72c-.28.8,7.1,26.77,19.23,23.45,5.54-1.52,6.4-7.65,6.73-12.61.23-3.59.11-7.19-.36-10.75,0,0-17.76-23.07-25.59-.08h-.01Z"/><path class="cls-32_scientist-72" d="M414.71,184.8c-.37.84-1.08,1.49-1.94,1.8-.86.3-1.77.43-2.67.39-.81.03-1.61-.12-2.35-.42-.69-.38-1.3-.86-1.82-1.45.27.36-1.25-1-4.86-3.83,0-3.01,1.5-9.47-1.68-8.61-1.24.34-1.26,3.7-1.39,3.93.14-.76-.89-2.61-1.36-3.99-2.62.12-5.41.62-9.04-4.02-5.93-7.57-12.28-7-12.28-7,3.77-2.47,8.68-8.08,18.86-6.51,4.54.71,6.44,4.4,7.12,8.29,1.18.59,2.3,1.27,3.36,2.05,3.57,2.72,5.66,6.96,6.98,11.25.55,1.77.99,3.58,1.64,5.31.36.99.84,1.94,1.44,2.81h-.01Z"/><path class="cls-33_scientist-72" d="M313.1,216.07c.98,1.68,6.83,1.44,8.2,2.17-.45,0-6.17-.25-7.66-.22-1.09,0-1.08,1.29-.28,1.68,1.95.99,6.48.69,8.04,1.14-.67-.25-6.28.35-6.99.41-.97.17-1.99,1.63,1.15,1.93,1.28.12,4.4,0,5.94.34.84.16-5.22.45-5.32,1.31-.21,1.75,6.04,1.3,6.51,1.35,2.94.28,8.63,1.05,10.88.84,0-2.35,1.52-5.52-.49-9.25-.3-.56-3.47-2.35-3.8-2.87-1.52-2.39-3.36-4.25-5.2-4.67-3.07-.69-.36,1.88-.24,3.96.16,2.64-.46,1.87-4.2,1.19-.78-.13-7.49-.89-6.53.71v-.02Z"/><path class="cls-33_scientist-72" d="M399.05,265.86c-2.3-.19-4.62.09-6.82.8-.13.03-.24.1-.33.2-.05.1-.07.2-.05.31.22.87.99,1.49,1.89,1.53.87.01,1.75-.04,2.61-.16.44,0,1.01.14,1.02.59,0,.14-.05.27-.13.39-.73.99-1.79,1.69-2.99,1.95-2.38.76-4.86,1.14-7.36,1.15-1.1-.06-2.2,0-3.3.14-.34.07-.74.23-.79.58,0,.27.15.52.38.67,1.55,1.29,3.76,1.31,5.78,1.25l-4.11.34c-.69-.02-1.37.19-1.93.59.36.65.97,1.12,1.68,1.3.71.19,1.44.28,2.18.27l3.31.08c-1.56-.05-3.11.24-4.55.84-.12.04-.22.11-.29.2-.15.26.14.56.41.71,2.3,1.21,5.04.9,7.64.55l-3.85.9c-.18.04-.39.13-.4.3,0,.08.04.16.1.21.25.21.57.32.9.29,2.77.26,5.56-.07,8.2-.94,1.18-.46,2.32-1,3.41-1.62.59-.29,1.15-.64,1.68-1.03.52-.46.99-.98,1.4-1.54.98-1.27,6-3.3,6.87-4.65.11-.15.19-.33.23-.52,0-.36.25-1.45,0-1.68-.89-.84-2.1-.89-2.52-2.03-.2-.5-2.61-1.49-2.82-1.98-.29-.68-2.52.34-3.21.39-1.43-.02-2.85-.15-4.26-.38h.02Z"/><path class="cls-34_scientist-72 targetColor" d="M413.53,276.74l-11.93-13.72s23.31-13.45,22.35-22.22-10.29-19.2-11.47-27.74c-1.19-8.54,12.98-11.08,12.98-11.08,9.6,10.29,11.64,28.05,15.97,42.3,3.82,12.39-27.9,32.46-27.9,32.46h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-21_scientist-72" d="M413.53,276.74l-6.73-7.77-5.18-5.95s23.31-13.45,22.35-22.22c-.14-1.21-.4-2.4-.78-3.56-2.52-7.94-9.67-16.77-10.69-24.16-1.21-8.51,12.95-11.1,12.95-11.1,9.6,10.29,11.64,28.05,15.97,42.3,3.82,12.39-27.9,32.46-27.9,32.46h0Z"/><path class="cls-34_scientist-72 targetColor" d="M408.09,211.36l2.09,7.43s-12.46,15.98-15.53,18.07c-3.08,2.08.5-4.97.5-4.97,0,0,7.37-14.57,7.94-18.7s5.01-1.83,5.01-1.83h-.01Z" style="fill: rgb(104, 225, 253);"/><path class="cls-7_scientist-72" d="M408.09,211.36l2.09,7.43s-12.46,15.98-15.53,18.07c-3.08,2.08.5-4.97.5-4.97,0,0,7.37-14.57,7.94-18.7s5.01-1.83,5.01-1.83h-.01Z"/><path class="cls-34_scientist-72 targetColor" d="M405.93,192.77s2.97.7,4.25,1.87c1.29,1.17,3.51,11.47,3.51,11.47l-11.96,11.2s4.98-19.65,4.19-24.53h0Z" style="fill: rgb(104, 225, 253);"/><path class="cls-22_scientist-72" d="M405.93,192.77s2.97.7,4.25,1.87c1.29,1.17,3.51,11.47,3.51,11.47l-11.96,11.2s4.98-19.65,4.19-24.53h0Z"/><path class="cls-34_scientist-72 targetColor" d="M396.65,198.9c-2.78,6.28-2.8,21.28-2.8,21.28l-6.82-10.69,8.49-13.41c.61.83,1,1.8,1.13,2.82Z" style="fill: rgb(104, 225, 253);"/><path class="cls-20_scientist-72" d="M396.65,198.9c-2.78,6.28-2.8,21.28-2.8,21.28l-6.82-10.69,8.49-13.41c.61.83,1,1.8,1.13,2.82Z"/><path class="cls-6_scientist-72" d="M430.03,374.44s-5.83-15.53-8.33-27.2c-2.5-11.68-3.73-47.3-3.73-47.3,2.76.93,5.62,1.54,8.52,1.82.29,1.2.44,2.42.44,3.66-.11,19.99-2.79,41.27,2.93,59.08,1.16,3.61,2.75,7.53.17,9.95h0Z"/><path class="cls-4_scientist-72" d="M333.94,220.19v.23c-.23-.2,0-.23,0-.23Z"/><path class="cls-5_scientist-72" d="M428.1,252.16c-2.01,5.67-21.32,16.81-21.32,16.81l-5.18-5.95s23.31-13.45,22.35-22.22c-.14-1.21-.4-2.4-.78-3.56,0,0,6.94,9.25,4.93,14.91h0Z"/><path class="cls-33_scientist-72" d="M398.22,177.89s1.68.14,1.21-1.22-.06-3.16.89-3.02.29,5.37-.34,5.78-1.76-1.54-1.76-1.54Z"/></g></svg>
1	t	2024-01-01 00:00:00+00	2025-09-12 18:51:53.054393+00	Mathématiques	2	Comprenez et maîtrisez les concepts clés	#4CAF50	<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 500 500" style="width: 175px;" xml:space="preserve" data-imageid="calculator-72" imageName="Calculator" class="illustrations_image">\n<style type="text/css">\n\t.st0_calculator-72{fill:#093F68;}\n\t.st1_calculator-72{fill:#68E1FD;}\n\t.st2_calculator-72{fill:#FFBC0E;}\n\t.st3_calculator-72{fill:#F56132;}\n\t.st4_calculator-72{fill:#FFFFFF;}\n</style>\n<g id="calculator_calculator-72">\n\t<path class="st0_calculator-72" d="M143.5,107.8h208c9.9,0,18,8,18,18v267.8c0,9.9-8,18-18,18h-208c-9.9,0-18-8-18-18V125.7&#10;&#9;&#9;C125.6,115.8,133.6,107.8,143.5,107.8z"/>\n\t<path class="st0_calculator-72" d="M352.7,413.3H142.4c-10.3,0-18.6-8.3-18.6-18.6V124.6c0-10.3,8.3-18.6,18.6-18.6h210.4&#10;&#9;&#9;c10.3,0,18.6,8.3,18.6,18.6v270.2C371.3,405,363,413.3,352.7,413.3z M142.4,109.6c-8.3,0-15,6.7-15,15v270.1c0,8.3,6.7,15,15,15&#10;&#9;&#9;h210.4c8.2,0,14.9-6.7,15-15V124.6c0-8.3-6.7-15-15-15L142.4,109.6z"/>\n\t<path class="st1_calculator-72 targetColor" d="M142.2,87.7h210.7c9.2,0,16.6,7.4,16.6,16.6v270.6c0,9.2-7.4,16.6-16.6,16.6H142.2c-9.2,0-16.6-7.4-16.6-16.6&#10;&#9;&#9;V104.2C125.6,95.1,133,87.7,142.2,87.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_calculator-72" d="M352.7,393.2H142.4c-10.3,0-18.6-8.3-18.6-18.6V104.4c0-10.3,8.3-18.6,18.6-18.6h210.4&#10;&#9;&#9;c10.3,0,18.6,8.3,18.6,18.6v270.2C371.3,384.9,363,393.2,352.7,393.2z M142.4,89.5c-8.3,0-15,6.7-15,15l0,0v270.1&#10;&#9;&#9;c0,8.3,6.7,14.9,15,14.9h210.4c8.2,0,14.9-6.7,15-14.9V104.4c0-8.3-6.7-15-15-15L142.4,89.5z"/>\n\t<path class="st2_calculator-72" d="M145.8,168.9h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C143.8,169.8,144.7,168.9,145.8,168.9z"/>\n\t<path class="st0_calculator-72" d="M182.7,213.3h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C188.2,210.8,185.7,213.3,182.7,213.3z M147.5,170.8c-1,0-1.9,0.8-1.9,1.8v0v35.2c0,1,0.8,1.9,1.8,1.9h0h35.2c1,0,1.8-0.8,1.8-1.8&#10;&#9;&#9;c0,0,0,0,0,0v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0H147.5z"/>\n\t<path class="st0_calculator-72" d="M167.4,182.5h-8.7V179h12.9v3.3l-7,14.3h-4.3L167.4,182.5z"/>\n\t<path class="st2_calculator-72" d="M200.6,168.9h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C198.6,169.8,199.5,168.9,200.6,168.9z"/>\n\t<path class="st0_calculator-72" d="M237.4,213.3h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C242.9,210.8,240.5,213.3,237.4,213.3z M202.3,170.8c-1,0-1.8,0.8-1.8,1.9v35.2c0,1,0.8,1.8,1.8,1.9h35.2c1,0,1.8-0.8,1.8-1.9&#10;&#9;&#9;v-35.2c0-1-0.8-1.8-1.8-1.9L202.3,170.8z"/>\n\t<path class="st0_calculator-72" d="M214,186c0-0.7,0.1-1.5,0.5-2.1c0.3-0.6,0.7-1.1,1.3-1.5c0.6-0.4,1.2-0.7,1.9-0.9c1.5-0.4,3.1-0.4,4.6,0&#10;&#9;&#9;c0.7,0.2,1.3,0.5,1.9,0.9c0.5,0.4,1,0.9,1.3,1.5c0.3,0.7,0.5,1.4,0.5,2.1c0,0.9-0.3,1.8-0.8,2.5c-0.6,0.7-1.3,1.2-2.2,1.4v0.1&#10;&#9;&#9;c2,0.4,3.4,2.2,3.3,4.3c0,1.5-0.7,2.9-1.9,3.8c-0.6,0.4-1.3,0.8-2,1c-1.5,0.4-3.1,0.4-4.7,0c-0.7-0.2-1.4-0.6-2-1&#10;&#9;&#9;c-1.2-0.9-1.9-2.3-1.9-3.8c-0.1-2.1,1.3-3.9,3.4-4.3v-0.1c-0.9-0.2-1.6-0.7-2.2-1.4C214.3,187.7,214,186.9,214,186z M217.4,193.7&#10;&#9;&#9;c0,0.6,0.2,1.2,0.7,1.6c1,0.9,2.5,0.9,3.6,0c0.9-0.8,0.9-2.2,0-3.1c0,0,0,0,0,0c-1-0.9-2.5-0.9-3.6,0&#10;&#9;&#9;C217.7,192.5,217.4,193.1,217.4,193.7L217.4,193.7z M217.7,186.5c0,0.5,0.2,1,0.6,1.4c0.9,0.8,2.2,0.8,3.1,0&#10;&#9;&#9;c0.4-0.4,0.6-0.9,0.6-1.4c0-0.5-0.2-1-0.6-1.4c-0.9-0.8-2.2-0.8-3.1,0C217.9,185.5,217.7,186,217.7,186.5L217.7,186.5z"/>\n\t<path class="st2_calculator-72" d="M255.4,168.9h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C253.4,169.8,254.3,168.9,255.4,168.9z"/>\n\t<path class="st0_calculator-72" d="M292.2,213.3H257c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5l0,0v35.2&#10;&#9;&#9;C297.7,210.8,295.2,213.3,292.2,213.3z M257,170.8c-1,0-1.8,0.8-1.8,1.8c0,0,0,0,0,0v35.2c0,1,0.8,1.8,1.8,1.8c0,0,0,0,0,0h35.2&#10;&#9;&#9;c1,0,1.9-0.8,1.9-1.8v0v-35.2c0-1-0.8-1.9-1.9-1.9l0,0H257z"/>\n\t<path class="st0_calculator-72" d="M274.8,192.9l-0.6,0.1c-0.2,0-0.4,0-0.6,0.1c-0.8,0-1.5-0.1-2.3-0.4c-0.7-0.3-1.3-0.7-1.7-1.2&#10;&#9;&#9;c-0.5-0.5-0.9-1.2-1.1-1.8c-0.3-0.7-0.4-1.5-0.4-2.2c0-0.8,0.2-1.7,0.5-2.5c0.3-0.7,0.8-1.4,1.4-1.9c0.6-0.5,1.3-1,2-1.2&#10;&#9;&#9;c1.7-0.6,3.5-0.6,5.1,0c0.8,0.3,1.5,0.7,2.1,1.2c1.2,1.1,1.9,2.7,1.9,4.4c0,0.6,0,1.1-0.1,1.7c-0.1,0.5-0.3,1-0.5,1.5&#10;&#9;&#9;c-0.2,0.5-0.4,0.9-0.7,1.3c-0.2,0.4-0.5,0.9-0.8,1.3l-3.9,6h-4.5L274.8,192.9z M271.8,187.4c0,0.7,0.3,1.5,0.8,2c1.2,1,2.9,1,4.1,0&#10;&#9;&#9;c1-1.1,1-2.8,0-3.9c-1.2-1-2.9-1-4.1,0C272.1,186,271.8,186.7,271.8,187.4L271.8,187.4z"/>\n\t<path class="st2_calculator-72" d="M310.1,168.9h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C308.1,169.8,309,168.9,310.1,168.9z"/>\n\t<path class="st0_calculator-72" d="M347,213.3h-35.2c-3,0-5.5-2.5-5.5-5.5l0,0v-35.2c0-3,2.5-5.5,5.5-5.5l0,0H347c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C352.5,210.8,350,213.3,347,213.3z M311.8,170.8c-1,0-1.9,0.8-1.9,1.8v0v35.2c0,1,0.8,1.9,1.9,1.9l0,0H347c1,0,1.8-0.8,1.8-1.8&#10;&#9;&#9;c0,0,0,0,0,0v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0H311.8z"/>\n\t<path class="st2_calculator-72" d="M145.8,220.8h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C143.8,221.7,144.7,220.8,145.8,220.8z"/>\n\t<path class="st0_calculator-72" d="M182.7,265.1h-35.2c-3,0-5.5-2.5-5.5-5.5l0,0v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C188.2,262.7,185.7,265.1,182.7,265.1z M147.5,222.6c-1,0-1.8,0.8-1.8,1.8c0,0,0,0,0,0v35.2c0,1,0.8,1.9,1.8,1.9h0h35.2&#10;&#9;&#9;c1,0,1.8-0.8,1.8-1.8c0,0,0,0,0,0v-35.2c0-1-0.8-1.8-1.8-1.8L147.5,222.6z"/>\n\t<path class="st0_calculator-72" d="M166,247.3h-7.7v-3.1l7.2-10.9h4.1v10.9h2.3v3.1h-2.3v3.5H166V247.3z M166,238.1L166,238.1l-3.9,6.1h3.9V238.1&#10;&#9;&#9;z"/>\n\t<path class="st2_calculator-72" d="M200.6,220.8h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C198.6,221.7,199.5,220.8,200.6,220.8z"/>\n\t<path class="st0_calculator-72" d="M237.4,265.1h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C242.9,262.7,240.5,265.1,237.4,265.1z M202.3,222.6c-1,0-1.8,0.8-1.8,1.8v35.2c0,1,0.8,1.8,1.8,1.9h35.2c1,0,1.8-0.8,1.8-1.9&#10;&#9;&#9;v-35.2c0-1-0.8-1.8-1.8-1.8L202.3,222.6z"/>\n\t<path class="st0_calculator-72" d="M225.6,236.4h-7l-0.1,2.7c0.5-0.1,1-0.2,1.6-0.2c0.8,0,1.7,0.1,2.5,0.4c0.7,0.2,1.4,0.6,1.9,1.1&#10;&#9;&#9;c0.5,0.5,1,1.1,1.3,1.8c0.3,0.8,0.5,1.6,0.4,2.4c0,0.9-0.2,1.8-0.5,2.7c-0.3,0.8-0.8,1.4-1.4,2c-0.6,0.6-1.3,1-2.1,1.2&#10;&#9;&#9;c-0.9,0.3-1.8,0.4-2.7,0.4c-1.4,0-2.7-0.3-3.8-1.1c-1.1-0.8-1.8-2-2.1-3.4l3.9-0.9c0.1,0.6,0.4,1.1,0.8,1.5c0.4,0.4,1,0.6,1.6,0.6&#10;&#9;&#9;c0.7,0,1.4-0.2,1.9-0.8c0.5-0.5,0.7-1.2,0.7-1.9c0-0.5-0.1-1-0.4-1.4c-0.2-0.4-0.6-0.7-0.9-0.9c-0.4-0.2-0.8-0.4-1.3-0.5&#10;&#9;&#9;c-0.5-0.1-1-0.1-1.4-0.1c-0.6,0-1.2,0.1-1.9,0.2c-0.6,0.1-1.2,0.3-1.8,0.5l0.2-9.7h10.6L225.6,236.4z"/>\n\t<path class="st2_calculator-72" d="M255.4,220.8h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C253.4,221.7,254.3,220.8,255.4,220.8z"/>\n\t<path class="st0_calculator-72" d="M292.2,265.1H257c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C297.7,262.7,295.2,265.1,292.2,265.1z M257,222.6c-1,0-1.8,0.8-1.8,1.8v35.2c0,1,0.8,1.8,1.8,1.8c0,0,0,0,0,0h35.2&#10;&#9;&#9;c1,0,1.9-0.8,1.9-1.9l0,0v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0L257,222.6z"/>\n\t<path class="st0_calculator-72" d="M274.5,239.4l0.6-0.1c0.2,0,0.4,0,0.6-0.1c0.8,0,1.5,0.1,2.2,0.4c0.7,0.3,1.3,0.7,1.7,1.2&#10;&#9;&#9;c0.5,0.5,0.9,1.1,1.1,1.8c0.3,0.7,0.4,1.5,0.4,2.2c0,0.9-0.2,1.7-0.5,2.5c-0.3,0.7-0.8,1.4-1.4,1.9c-0.6,0.5-1.3,1-2.1,1.2&#10;&#9;&#9;c-1.7,0.6-3.5,0.6-5.1,0c-0.8-0.3-1.5-0.7-2.1-1.2c-0.6-0.5-1.1-1.2-1.4-1.9c-0.3-0.8-0.5-1.6-0.5-2.5c0-0.6,0-1.2,0.2-1.7&#10;&#9;&#9;c0.1-0.5,0.3-1,0.5-1.5c0.2-0.5,0.4-0.9,0.7-1.3l0.8-1.3l3.9-6h4.5L274.5,239.4z M277.5,244.8c0-0.7-0.3-1.5-0.8-2&#10;&#9;&#9;c-0.5-0.5-1.3-0.8-2-0.8c-0.8,0-1.5,0.3-2,0.8c-1,1.1-1,2.8,0,3.9c0.5,0.5,1.3,0.8,2,0.8c0.8,0,1.5-0.3,2-0.8&#10;&#9;&#9;C277.2,246.2,277.5,245.5,277.5,244.8z"/>\n\t<path class="st2_calculator-72" d="M310.1,220.8h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C308.1,221.7,309,220.8,310.1,220.8z"/>\n\t<path class="st0_calculator-72" d="M347,265.1h-35.2c-3,0-5.5-2.5-5.5-5.5c0,0,0,0,0,0v-35.2c0-3,2.5-5.5,5.5-5.5H347c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C352.5,262.7,350,265.1,347,265.1z M311.8,222.6c-1,0-1.8,0.8-1.8,1.8c0,0,0,0,0,0v35.2c0,1,0.8,1.9,1.9,1.9l0,0H347&#10;&#9;&#9;c1,0,1.8-0.8,1.8-1.8c0,0,0,0,0,0v-35.2c0-1-0.8-1.8-1.8-1.8L311.8,222.6z"/>\n\t<path class="st2_calculator-72" d="M145.8,272.6h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C143.8,273.5,144.7,272.6,145.8,272.6z"/>\n\t<path class="st0_calculator-72" d="M182.7,317h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5l0,0h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C188.2,314.5,185.7,317,182.7,317L182.7,317z M147.5,274.5c-1,0-1.9,0.8-1.9,1.9l0,0v35.2c0,1,0.8,1.8,1.8,1.8c0,0,0,0,0,0h35.2&#10;&#9;&#9;c1,0,1.8-0.8,1.8-1.8v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0H147.5z"/>\n\t<path class="st0_calculator-72" d="M166.1,289.3l-3.5,3.1l-2.1-2.4l5.7-4.8h3.5v17.5h-3.6V289.3z"/>\n\t<path class="st2_calculator-72" d="M200.6,272.6h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C198.6,273.5,199.5,272.6,200.6,272.6z"/>\n\t<path class="st0_calculator-72" d="M237.4,317h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C242.9,314.5,240.5,317,237.4,317z M202.3,274.5c-1,0-1.8,0.8-1.8,1.9v35.2c0,1,0.8,1.8,1.8,1.8h35.2c1,0,1.8-0.8,1.8-1.8v-35.2&#10;&#9;&#9;c0-1-0.8-1.8-1.8-1.9H202.3z"/>\n\t<path class="st0_calculator-72" d="M213.7,298.9l6.8-6.1c0.4-0.3,0.7-0.7,1-1.1c0.3-0.4,0.5-0.9,0.5-1.4c0-0.5-0.2-1.1-0.6-1.4&#10;&#9;&#9;c-0.4-0.3-1-0.5-1.5-0.5c-0.6,0-1.2,0.2-1.6,0.6c-0.4,0.4-0.6,1-0.7,1.6l-3.7-0.3c0-0.8,0.2-1.6,0.6-2.4c0.3-0.6,0.8-1.2,1.3-1.7&#10;&#9;&#9;c0.6-0.5,1.2-0.8,1.9-1c0.8-0.2,1.6-0.3,2.4-0.3c0.8,0,1.5,0.1,2.2,0.3c0.7,0.2,1.3,0.6,1.8,1c0.5,0.5,0.9,1,1.2,1.6&#10;&#9;&#9;c0.3,0.7,0.5,1.5,0.4,2.3c0,0.5-0.1,1-0.2,1.5c-0.1,0.4-0.3,0.9-0.5,1.2c-0.2,0.4-0.5,0.7-0.7,1c-0.3,0.3-0.6,0.6-0.9,0.9l-5.3,4.6&#10;&#9;&#9;h7.8v3.3h-12.3V298.9z"/>\n\t<path class="st2_calculator-72" d="M255.4,272.6h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C253.4,273.5,254.3,272.6,255.4,272.6z"/>\n\t<path class="st0_calculator-72" d="M292.2,317H257c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5c0,0,0,0,0,0v35.2&#10;&#9;&#9;C297.7,314.5,295.2,317,292.2,317z M257,274.5c-1,0-1.8,0.8-1.8,1.8c0,0,0,0,0,0v35.2c0,1,0.8,1.8,1.8,1.8h35.2&#10;&#9;&#9;c1,0,1.8-0.8,1.8-1.8c0,0,0,0,0,0v-35.2c0-1-0.8-1.9-1.9-1.9l0,0H257z"/>\n\t<path class="st0_calculator-72" d="M272.9,292h1.2c0.3,0,0.7,0,1-0.1c0.3,0,0.6-0.1,0.9-0.3c0.3-0.1,0.5-0.3,0.7-0.6c0.2-0.3,0.3-0.6,0.2-1&#10;&#9;&#9;c0-0.5-0.2-1-0.6-1.3c-0.4-0.4-1-0.5-1.6-0.5c-0.5,0-1,0.1-1.4,0.5c-0.4,0.3-0.6,0.7-0.7,1.2l-4.1-0.8c0.2-0.7,0.5-1.4,0.9-2&#10;&#9;&#9;c0.4-0.5,0.9-1,1.4-1.3c0.6-0.3,1.2-0.6,1.8-0.7c0.7-0.2,1.4-0.2,2.1-0.2c0.8,0,1.5,0.1,2.2,0.3c0.7,0.2,1.3,0.5,1.9,0.9&#10;&#9;&#9;c0.5,0.4,1,0.9,1.3,1.5c0.3,0.7,0.5,1.4,0.5,2.2c0,0.9-0.2,1.8-0.8,2.5c-0.5,0.7-1.3,1.2-2.2,1.3v0.1c0.5,0.1,1,0.2,1.4,0.5&#10;&#9;&#9;c0.4,0.2,0.7,0.5,1,0.9c0.3,0.4,0.5,0.8,0.6,1.2c0.1,0.5,0.2,1,0.2,1.5c0,0.8-0.2,1.6-0.5,2.3c-0.3,0.6-0.8,1.2-1.4,1.6&#10;&#9;&#9;c-0.6,0.5-1.3,0.8-2,1c-0.8,0.2-1.6,0.3-2.4,0.3c-1.4,0-2.8-0.3-4.1-1.1c-1.2-0.8-2-2-2.2-3.5l3.9-0.9c0.1,0.6,0.4,1.1,0.8,1.5&#10;&#9;&#9;c0.5,0.4,1.2,0.6,1.8,0.5c1.2,0.2,2.2-0.7,2.4-1.8c0-0.1,0-0.3,0-0.4c0-0.4-0.1-0.8-0.3-1.2c-0.2-0.3-0.5-0.5-0.8-0.6&#10;&#9;&#9;c-0.4-0.1-0.7-0.2-1.1-0.2c-0.4,0-0.8,0-1.2,0h-0.9L272.9,292z"/>\n\t<path class="st2_calculator-72" d="M310.1,272.6h38.5c1.1,0,2,0.9,2,2v38.5c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C308.1,273.5,309,272.6,310.1,272.6z"/>\n\t<path class="st0_calculator-72" d="M347,317h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5c0,0,0,0,0,0H347c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C352.5,314.5,350,317,347,317L347,317z M311.8,274.5c-1,0-1.9,0.8-1.9,1.9l0,0v35.2c0,1,0.8,1.8,1.8,1.8c0,0,0,0,0,0H347&#10;&#9;&#9;c1,0,1.8-0.8,1.8-1.8v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0H311.8z"/>\n\t<path class="st2_calculator-72" d="M145.8,324.5h38.5c1.1,0,2,0.9,2,2V365c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C143.8,325.4,144.7,324.5,145.8,324.5z"/>\n\t<path class="st0_calculator-72" d="M182.7,368.9h-35.2c-3,0-5.5-2.5-5.5-5.5l0,0v-35.2c0-3,2.5-5.5,5.5-5.5l0,0h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C188.2,366.4,185.7,368.9,182.7,368.9z M147.5,326.3c-1,0-1.9,0.8-1.9,1.9l0,0v35.2c0,1,0.8,1.9,1.8,1.9h0h35.2&#10;&#9;&#9;c1,0,1.8-0.8,1.8-1.8c0,0,0,0,0,0v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0H147.5z"/>\n\t<path class="st0_calculator-72" d="M158.6,343.4c0-1.1,0.1-2.1,0.3-3.2c0.2-1,0.5-2,1-2.9c0.5-0.9,1.2-1.6,2-2.1c2-1.1,4.4-1.1,6.5,0&#10;&#9;&#9;c0.8,0.5,1.5,1.3,2,2.1c0.5,0.9,0.8,1.9,1,2.9c0.4,2.1,0.4,4.3,0,6.4c-0.2,1-0.5,2-1,2.9c-0.5,0.9-1.2,1.6-2,2.1&#10;&#9;&#9;c-2,1.1-4.4,1.1-6.5,0c-0.8-0.5-1.5-1.3-2-2.1c-0.5-0.9-0.8-1.9-1-2.9C158.7,345.5,158.6,344.4,158.6,343.4z M162.3,343.4&#10;&#9;&#9;c0,0.5,0,1,0.1,1.7c0,0.6,0.2,1.3,0.3,1.9c0.2,0.6,0.4,1.1,0.8,1.5c0.9,0.8,2.3,0.8,3.1,0c0.4-0.4,0.7-1,0.9-1.5&#10;&#9;&#9;c0.2-0.6,0.3-1.2,0.3-1.9c0-0.6,0.1-1.2,0.1-1.7s0-1-0.1-1.7c0-0.6-0.1-1.3-0.3-1.9c-0.2-0.6-0.5-1.1-0.9-1.5&#10;&#9;&#9;c-0.9-0.8-2.3-0.8-3.1,0c-0.4,0.4-0.7,1-0.8,1.5c-0.2,0.6-0.3,1.2-0.3,1.9C162.3,342.4,162.3,342.9,162.3,343.4z"/>\n\t<path class="st2_calculator-72" d="M200.6,324.5h38.5c1.1,0,2,0.9,2,2V365c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C198.6,325.4,199.5,324.5,200.6,324.5z"/>\n\t<path class="st0_calculator-72" d="M237.4,368.9h-35.2c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5v35.2&#10;&#9;&#9;C242.9,366.4,240.5,368.9,237.4,368.9z M202.3,326.3c-1,0-1.8,0.8-1.8,1.9v35.2c0,1,0.8,1.8,1.8,1.9h35.2c1,0,1.8-0.8,1.8-1.9&#10;&#9;&#9;v-35.2c0-1-0.8-1.8-1.8-1.9L202.3,326.3z"/>\n\t<path class="st2_calculator-72" d="M255.4,324.5h38.5c1.1,0,2,0.9,2,2V365c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C253.4,325.4,254.3,324.5,255.4,324.5z"/>\n\t<path class="st0_calculator-72" d="M292.2,368.9H257c-3,0-5.5-2.5-5.5-5.5v-35.2c0-3,2.5-5.5,5.5-5.5h35.2c3,0,5.5,2.5,5.5,5.5c0,0,0,0,0,0v35.2&#10;&#9;&#9;C297.7,366.4,295.2,368.8,292.2,368.9z M257,326.3c-1,0-1.8,0.8-1.8,1.8c0,0,0,0,0,0v35.2c0,1,0.8,1.8,1.8,1.8c0,0,0,0,0,0h35.2&#10;&#9;&#9;c1,0,1.9-0.8,1.9-1.9l0,0v-35.2c0-1-0.8-1.9-1.9-1.9l0,0H257z"/>\n\t<path class="st2_calculator-72" d="M310.1,324.5h38.5c1.1,0,2,0.9,2,2V365c0,1.1-0.9,2-2,2h-38.5c-1.1,0-2-0.9-2-2v-38.5&#10;&#9;&#9;C308.1,325.4,309,324.5,310.1,324.5z"/>\n\t<path class="st0_calculator-72" d="M347,368.9h-35.2c-3,0-5.5-2.5-5.5-5.5c0,0,0,0,0,0v-35.2c0-3,2.5-5.5,5.5-5.5c0,0,0,0,0,0H347&#10;&#9;&#9;c3,0,5.5,2.5,5.5,5.5v35.2C352.5,366.4,350,368.9,347,368.9z M311.8,326.3c-1,0-1.9,0.8-1.9,1.9l0,0v35.2c0,1,0.8,1.9,1.9,1.9l0,0&#10;&#9;&#9;H347c1,0,1.8-0.8,1.8-1.8c0,0,0,0,0,0v-35.2c0-1-0.8-1.8-1.8-1.8c0,0,0,0,0,0H311.8z"/>\n\t<circle class="st0_calculator-72" cx="219.9" cy="345.7" r="4.1"/>\n\t<path class="st0_calculator-72" d="M321.6,199.9c-0.5,0-0.9-0.2-1.3-0.5c-0.7-0.7-0.7-1.9,0-2.6l15.5-15.8c0.7-0.7,1.9-0.7,2.6,0s0.7,1.9,0,2.6&#10;&#9;&#9;l0,0l-15.5,15.8C322.6,199.7,322.1,199.9,321.6,199.9z"/>\n\t<path class="st0_calculator-72" d="M321.6,251.8c-1,0-1.8-0.8-1.8-1.9c0-0.5,0.2-0.9,0.5-1.2l15.5-15.8c0.7-0.8,1.8-0.8,2.6-0.1&#10;&#9;&#9;c0.8,0.7,0.8,1.8,0.1,2.6c0,0-0.1,0.1-0.1,0.1l-15.5,15.8C322.6,251.6,322.1,251.8,321.6,251.8z"/>\n\t<path class="st0_calculator-72" d="M337.2,251.8c-0.5,0-1-0.2-1.3-0.6l-15.5-15.8c-0.7-0.7-0.7-1.9,0-2.6s1.9-0.7,2.6,0l0,0l15.5,15.8&#10;&#9;&#9;c0.7,0.7,0.7,1.9,0,2.6C338.1,251.6,337.6,251.8,337.2,251.8z"/>\n\t<path class="st0_calculator-72" d="M337.4,295.7h-15.9c-1,0-1.8-0.8-1.8-1.8c0-1,0.8-1.8,1.8-1.8h15.9c1,0,1.8,0.8,1.8,1.8&#10;&#9;&#9;C339.2,294.9,338.4,295.7,337.4,295.7z"/>\n\t<path class="st0_calculator-72" d="M337.4,342.3h-15.9c-1,0-1.8-0.8-1.8-1.8c0-1,0.8-1.8,1.8-1.8h15.9c1,0,1.8,0.8,1.8,1.8&#10;&#9;&#9;C339.2,341.5,338.4,342.3,337.4,342.3z"/>\n\t<path class="st0_calculator-72" d="M337.4,352.9h-15.9c-1,0-1.8-0.8-1.8-1.8c0-1,0.8-1.8,1.8-1.8h15.9c1,0,1.8,0.8,1.8,1.8&#10;&#9;&#9;C339.2,352.1,338.4,352.9,337.4,352.9z"/>\n\t<path class="st0_calculator-72" d="M282.6,347.6h-15.9c-1,0-1.8-0.8-1.8-1.8c0-1,0.8-1.8,1.8-1.8h15.9c1,0,1.8,0.8,1.8,1.8&#10;&#9;&#9;C284.4,346.8,283.6,347.6,282.6,347.6L282.6,347.6z"/>\n\t<path class="st0_calculator-72" d="M274.6,355.5c-1,0-1.8-0.8-1.8-1.8v-15.9c0-1,0.8-1.8,1.8-1.8c1,0,1.8,0.8,1.8,1.8v15.9&#10;&#9;&#9;C276.5,354.7,275.6,355.5,274.6,355.5L274.6,355.5z"/>\n\t<rect x="143.8" y="105.5" class="st3_calculator-72" width="206.8" height="47.6"/>\n\t<path class="st0_calculator-72" d="M350.6,154.9H143.8c-1,0-1.8-0.8-1.8-1.8l0,0v-47.6c0-1,0.8-1.8,1.8-1.8l0,0h206.8c1,0,1.8,0.8,1.8,1.8v47.6&#10;&#9;&#9;C352.5,154.1,351.7,154.9,350.6,154.9z M145.6,151.3h203.2v-43.9H145.6V151.3z"/>\n\t<path class="st4_calculator-72" d="M328.8,145.9h-7.6c-3.3,0-6.1-2.7-6.1-6.1V118c0-3.3,2.7-6.1,6.1-6.1h7.6c3.3,0,6.1,2.7,6.1,6.1v21.8&#10;&#9;&#9;C334.8,143.2,332.1,145.9,328.8,145.9z M321.2,115.6c-1.3,0-2.4,1.1-2.4,2.4v21.8c0,1.3,1.1,2.4,2.4,2.4h7.6c1.3,0,2.4-1.1,2.4-2.4&#10;&#9;&#9;V118c0-1.3-1.1-2.4-2.4-2.4L321.2,115.6z"/>\n\t<path class="st4_calculator-72" d="M332.2,144.1c-0.6,0-1.2-0.3-1.6-0.9L315.5,119c-0.6-0.8-0.4-2,0.5-2.5c0.8-0.6,2-0.4,2.5,0.5&#10;&#9;&#9;c0,0,0.1,0.1,0.1,0.1l15.2,24.3c0.5,0.9,0.3,2-0.6,2.5c0,0,0,0,0,0C332.9,144.1,332.5,144.2,332.2,144.1z"/>\n</g>\n</svg>
22	t	2025-08-15 07:40:15.264046+00	2025-09-12 19:10:11.550922+00	Informatique	0	Devenez acteur du monde digital	#3b82f6	<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 500 500" style="width: 175px;" xml:space="preserve" data-imageid="coding-2-31" imageName="Coding 2" class="illustrations_image">\n<style type="text/css">\n\t.st0_coding-2-31{fill:#FFFFFF;}\n\t.st1_coding-2-31{fill:#231F20;}\n\t.st2_coding-2-31{fill:#68E1FD;}\n\t.st3_coding-2-31{fill:#D1D3D4;}\n</style>\n<g id="Screen_1_coding-2-31">\n\t<path class="st0_coding-2-31" d="M132.6,243.8c0,0-1.7,41.2,2.9,54.8h21.1c2.2,0,4.2,1.5,4.9,3.6l1.1,3.8h-53.8c-4.1-2.7-7.5-6.2-10-10.3&#10;&#9;&#9;c-3.6-6.4-1.4-51.8-1.4-51.8H132.6z"/>\n\t<path class="st1_coding-2-31" d="M162.6,306.6h-53.8c-0.1,0-0.2,0-0.3-0.1c-4.1-2.7-7.6-6.3-10.2-10.5c-3.7-6.5-1.6-50.3-1.5-52.2&#10;&#9;&#9;c0-0.3,0.3-0.6,0.7-0.6h35c0.2,0,0.3,0.1,0.5,0.2c0.1,0.1,0.2,0.3,0.2,0.5c0,0.4-1.6,40.4,2.7,54.1h20.7c2.5,0,4.8,1.6,5.5,4.1&#10;&#9;&#9;l1.1,3.8c0.1,0.4-0.1,0.7-0.5,0.8C162.7,306.6,162.6,306.6,162.6,306.6z M109,305.3h52.7l-0.9-3c-0.6-1.9-2.3-3.1-4.2-3.1h-21.1&#10;&#9;&#9;c-0.3,0-0.5-0.2-0.6-0.4c-4.4-12.7-3.2-48.7-3-54.3H98.1c-0.8,15.9-1.4,46,1.3,50.9C101.9,299.3,105.1,302.7,109,305.3z"/>\n\t<path class="st1_coding-2-31" d="M100.1,287.7c0,8.6,2.6,11.2,6,11.2h13.5c1.9,0,3.6,1.2,4.3,3l1.5,4.1h-20.8c-5.3,0-9.1-8.1-9.3-16.7&#10;&#9;&#9;s0-45.5,0-45.5h4.6C99.9,243.8,100.1,279.1,100.1,287.7z"/>\n\t<path class="st1_coding-2-31" d="M125.3,306.6h-20.8c-6,0-9.8-8.8-9.9-17.3s0-45.1,0-45.5c0-0.4,0.3-0.6,0.7-0.6h4.6c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;c0,0.4,0.2,35.5,0.2,44c0,10.5,4,10.5,5.4,10.5h13.5c2.2,0,4.1,1.4,4.9,3.4l1.5,4.1c0.1,0.2,0,0.4-0.1,0.6&#10;&#9;&#9;C125.7,306.5,125.5,306.6,125.3,306.6z M95.9,244.4c0,5-0.2,37,0,44.8c0.2,8.8,4,16,8.6,16h19.8l-1.2-3.2c-0.6-1.5-2-2.5-3.7-2.5&#10;&#9;&#9;h-13.5c-4.5,0-6.7-3.9-6.7-11.8s-0.1-38.4-0.2-43.3L95.9,244.4z"/>\n\t<path class="st1_coding-2-31" d="M172.6,147.4l8.1,93c0.5,4-2.3,7.7-6.4,8.3c-0.3,0-0.6,0.1-0.9,0.1H62.6c-4.6-0.2-8.3-3.7-8.7-8.3l-8.1-93&#10;&#9;&#9;c-0.5-4,2.3-7.7,6.4-8.3c0.3,0,0.6-0.1,0.9-0.1h110.9C168.5,139.3,172.2,142.8,172.6,147.4z"/>\n\t<path class="st1_coding-2-31" d="M173.5,249.4H62.6c-4.9-0.2-9-4-9.4-8.9l-8.1-93c-0.2-2.4,0.5-4.7,2.1-6.5c1.5-1.6,3.6-2.6,5.8-2.6h110.9&#10;&#9;&#9;c4.9,0.2,8.9,4,9.4,8.9l8.1,93c0.2,2.4-0.5,4.7-2.1,6.5C177.8,248.5,175.7,249.4,173.5,249.4z M53,139.7c-1.8,0-3.6,0.7-4.8,2.1&#10;&#9;&#9;c-1.3,1.5-2,3.5-1.8,5.5l8.1,93c0.4,4.3,3.8,7.6,8.1,7.7h110.9c1.8,0,3.6-0.7,4.9-2.1c1.3-1.5,2-3.5,1.8-5.5l-8.1-93l0,0&#10;&#9;&#9;c-0.4-4.2-3.8-7.6-8.1-7.7L53,139.7z"/>\n\t<path class="st0_coding-2-31" d="M173,147l7.8,88.8c0.5,3.9-2.2,7.4-6,7.9c-0.3,0-0.6,0.1-1,0.1H68c-4.4-0.2-8-3.6-8.3-8L51.8,147&#10;&#9;&#9;c-0.5-3.8,2.2-7.4,6-7.9c0.3,0,0.6-0.1,1-0.1h105.9C169.1,139.2,172.6,142.6,173,147z"/>\n\t<path class="st1_coding-2-31" d="M173.8,244.4H68c-4.7-0.2-8.6-3.8-9-8.5l-7.8-88.8c-0.3-2.3,0.5-4.5,2-6.2c1.4-1.6,3.5-2.4,5.6-2.4h105.9&#10;&#9;&#9;c4.7,0.2,8.6,3.8,9,8.5l0,0l7.8,88.8c0.3,2.3-0.5,4.5-2,6.2C178,243.6,176,244.4,173.8,244.4z M58.8,139.7c-1.8,0-3.4,0.7-4.6,2&#10;&#9;&#9;c-1.3,1.4-1.9,3.3-1.7,5.3l7.8,88.8c0.3,4.1,3.7,7.2,7.7,7.3h105.8c1.8,0,3.4-0.7,4.6-2c1.3-1.4,1.9-3.3,1.7-5.2l-7.8-88.8&#10;&#9;&#9;c-0.3-4-3.6-7.2-7.7-7.4L58.8,139.7z"/>\n\t<path class="st0_coding-2-31" d="M179.5,220.9l1.3,14.9c0.5,3.9-2.2,7.4-6,7.9c-0.3,0-0.6,0.1-1,0.1H68c-4.4-0.2-8-3.6-8.3-8l-1.3-14.9H179.5z"/>\n\t<path class="st1_coding-2-31" d="M173.8,244.4H68c-4.7-0.2-8.6-3.8-9-8.5L57.7,221c0-0.2,0-0.4,0.2-0.5c0.1-0.1,0.3-0.2,0.5-0.2h121.2&#10;&#9;&#9;c0.3,0,0.6,0.3,0.6,0.6l1.3,14.9c0.3,2.3-0.5,4.5-2,6.2C178,243.6,175.9,244.4,173.8,244.4z M59,221.6l1.2,14.2&#10;&#9;&#9;c0.3,4.1,3.7,7.2,7.8,7.4h105.8c1.8,0,3.4-0.7,4.6-2c1.3-1.4,1.9-3.3,1.7-5.2l-1.2-14.3H59z"/>\n\t\n\t\t<ellipse transform="matrix(0.8307 -0.5567 0.5567 0.8307 -109.0576 106.0802)" class="st0_coding-2-31" cx="119.9" cy="232.3" rx="4.8" ry="5.3"/>\n\t<path class="st1_coding-2-31" d="M120.3,238.1c-3.2-0.1-5.7-2.6-6-5.7c-0.2-1.5,0.3-3.1,1.4-4.2c1-1.1,2.3-1.7,3.8-1.6c3.2,0.1,5.7,2.6,6,5.7&#10;&#9;&#9;l0,0c0.2,1.5-0.3,3.1-1.4,4.2C123.2,237.6,121.8,238.2,120.3,238.1z M119.4,227.8c-1.1,0-2.1,0.4-2.8,1.2c-0.8,0.9-1.1,2.1-1,3.2&#10;&#9;&#9;c0.2,2.5,2.2,4.4,4.8,4.6c1.1,0,2.1-0.4,2.8-1.2c0.8-0.9,1.1-2.1,1-3.2l0,0C124,229.9,121.9,228,119.4,227.8z"/>\n\t<path class="st1_coding-2-31" d="M60.3,145h103.8c2.3,0.1,4.1,1.9,4.3,4.1l5.5,62.6c0.3,2-1.2,3.8-3.2,4.1c-0.1,0-0.3,0-0.5,0H66.5&#10;&#9;&#9;c-2.3-0.1-4.1-1.9-4.3-4.1l-5.5-62.6c-0.3-2,1.1-3.8,3.1-4.1C60,145,60.2,145,60.3,145z"/>\n\t<path class="st0_coding-2-31" d="M77.8,152.7H67.5c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C78.5,152.4,78.2,152.7,77.8,152.7z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M101.1,152.7H80.5c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h20.6c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C101.7,152.4,101.4,152.7,101.1,152.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M108.3,156.7H87.8c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h20.6c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C109,156.4,108.7,156.7,108.3,156.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M80.4,156.7H70.1c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C81,156.4,80.7,156.7,80.4,156.7z"/>\n\t<path class="st0_coding-2-31" d="M83,160.8H72.7c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7H83c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C83.7,160.5,83.4,160.8,83,160.8z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M112.2,160.8H86.4c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h25.8c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C112.8,160.5,112.5,160.8,112.2,160.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M85.6,164.8H75.2c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6l0,0h10.3c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C86.2,164.5,85.9,164.8,85.6,164.8z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M117.7,164.8H87c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6h30.7c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C118.3,164.5,118,164.8,117.7,164.8L117.7,164.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M83,168.8H72.7c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6l0,0H83c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C83.7,168.5,83.4,168.8,83,168.8z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M101.7,168.8H85.1c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6h16.6c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C102.4,168.5,102.1,168.8,101.7,168.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M124.7,168.8h-16.6c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6h16.6c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C125.3,168.5,125,168.8,124.7,168.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M83.2,172.9H72.8c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C83.8,172.6,83.5,172.9,83.2,172.9z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M101.9,172.9H87.4c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h14.5c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C102.5,172.6,102.2,172.9,101.9,172.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M110.3,172.9h-5.9c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h5.9c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C110.9,172.6,110.6,172.9,110.3,172.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M83.3,176.9H73c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C84,176.6,83.7,176.9,83.3,176.9z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M107.2,176.9H86.1c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h21.2c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C107.9,176.6,107.6,176.9,107.2,176.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M120.1,176.9h-10.3c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C120.7,176.6,120.4,176.9,120.1,176.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M76.2,181h-5.5c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h5.5c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C76.8,180.7,76.6,181,76.2,181z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M104.7,181H80.7c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h23.9c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C105.3,180.7,105,181,104.7,181z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M81.2,185H70.9c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C81.9,184.7,81.6,185,81.2,185z"/>\n\t<path class="st0_coding-2-31" d="M93.2,189H72.6c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h20.6c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C93.8,188.7,93.5,189,93.2,189z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M110.9,189H96.6c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h14.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C111.6,188.7,111.3,189,110.9,189z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M130.7,189H113c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h17.7c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C131.4,188.7,131.1,189,130.7,189L130.7,189z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M103.7,193.1h-30c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h30c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C104.3,192.8,104,193.1,103.7,193.1z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M119.2,193.1h-13.5c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h13.5c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C119.9,192.8,119.6,193.1,119.2,193.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M161.7,193.1h-40.2c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h40.2c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C162.3,192.8,162,193.1,161.7,193.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M87.9,197.1H73.7c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h14.2c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C88.5,196.8,88.2,197.1,87.9,197.1z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M101.2,197.1H90.7c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.5c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C101.8,196.8,101.5,197.1,101.2,197.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M114.4,197.1H104c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.4c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C115.1,196.8,114.8,197.1,114.4,197.1L114.4,197.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M99,201.1H73.8c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6H99c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C99.7,200.8,99.4,201.1,99,201.1z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M114.6,201.1H102c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6l0,0h12.6c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C115.2,200.8,115,201.1,114.6,201.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M136.8,201.1h-19.1c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6l0,0h19.1c0.4,0,0.7,0.3,0.7,0.6&#10;&#9;&#9;C137.5,200.8,137.2,201.1,136.8,201.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M157.9,201.1h-19.1c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h19.1c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C158.6,200.8,158.3,201.1,157.9,201.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M95.3,205.2h-15c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h15c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C96,204.9,95.7,205.2,95.3,205.2z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M113.1,205.2h-15c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h15c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C113.8,204.9,113.5,205.2,113.1,205.2z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M131,205.2h-15c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h15c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C131.6,204.9,131.4,205.2,131,205.2z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M149.6,205.6h-15c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h15c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C150.2,205.3,149.9,205.6,149.6,205.6z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M93.1,209.2H82.8c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C93.7,208.9,93.4,209.2,93.1,209.2z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M105.8,209.2H95.5c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h10.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C106.5,208.9,106.2,209.2,105.8,209.2z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M129.7,209.6L129.7,209.6l-21.3-0.4c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0l21.3,0.4&#10;&#9;&#9;c0.4,0,0.7,0.3,0.7,0.7C130.3,209.3,130,209.6,129.7,209.6L129.7,209.6z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M135.8,164.8h-14c-0.4,0-0.7-0.3-0.7-0.7c0-0.4,0.3-0.6,0.7-0.6h14c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C136.5,164.5,136.2,164.8,135.8,164.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M146.1,164.8c-1.7,0.1-3.3,0-5-0.1c-0.3-0.1-0.5-0.5-0.4-0.8c0.1-0.3,0.4-0.5,0.7-0.4c0.7,0.1,9.8,0,15.8,0&#10;&#9;&#9;l0,0c0.4,0,0.6,0.3,0.6,0.6c0,0.4-0.3,0.6-0.6,0.6c0,0,0,0,0,0C152,164.8,148.5,164.8,146.1,164.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M133.3,156.7H113c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7l0,0h20.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C133.9,156.4,133.6,156.7,133.3,156.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M157.5,156.7h-20.2c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h20.2c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C158.1,156.4,157.8,156.7,157.5,156.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M114.4,152.7c-4.1,0-7,0-7.1,0c-0.4,0-0.6-0.4-0.6-0.7c0-0.3,0.4-0.6,0.7-0.6c0.7,0,17,0,23.3,0l0,0&#10;&#9;&#9;c0.4,0,0.6,0.3,0.6,0.6c0,0.4-0.3,0.7-0.6,0.7L114.4,152.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M136.3,152.7c-0.3,0-0.5-0.1-0.6-0.4c-0.2-0.3,0-0.7,0.3-0.9c0.2-0.1,0.4-0.2,14.1-0.1c0.3,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;c0,0,0,0,0,0c0,0.4-0.3,0.6-0.7,0.6c-4.9-0.1-12.9-0.1-13.7,0H136.3z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M117.9,181h-10.4c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h10.4c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C118.5,180.7,118.2,181,117.9,181z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M94.1,185h-7.7c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h7.7c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C94.7,184.7,94.4,185,94.1,185z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M115.2,185H97c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h18.3c0.4,0,0.7,0.3,0.7,0.7&#10;&#9;&#9;C115.9,184.7,115.6,185,115.2,185L115.2,185z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M154.3,185h-35.4c-0.4,0-0.7-0.3-0.7-0.6c0-0.4,0.3-0.7,0.7-0.7h35.4c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C154.9,184.7,154.6,185,154.3,185z" style="fill: rgb(104, 225, 253);"/>\n</g>\n<g id="Screen_2_coding-2-31">\n\t<path class="st0_coding-2-31" d="M348.1,243.8c0,0,1.7,41.2-2.9,54.8h-21.1c-2.2,0-4.2,1.5-4.9,3.6l-1.1,3.8h53.8c4.1-2.7,7.5-6.2,10-10.3&#10;&#9;&#9;c3.6-6.4,1.4-51.8,1.4-51.8H348.1z"/>\n\t<path class="st1_coding-2-31" d="M371.9,306.6h-53.8c-0.2,0-0.4-0.1-0.5-0.3c-0.1-0.2-0.2-0.4-0.1-0.6l1.1-3.8c0.7-2.4,2.9-4.1,5.5-4.1h20.7&#10;&#9;&#9;c4.4-13.7,2.7-53.7,2.7-54.1c0-0.2,0.1-0.3,0.2-0.5c0.1-0.1,0.3-0.2,0.5-0.2h35.1c0.3,0,0.6,0.3,0.6,0.6c0.1,1.9,2.2,45.8-1.5,52.2&#10;&#9;&#9;c-2.6,4.2-6,7.8-10.2,10.5C372.1,306.5,372,306.6,371.9,306.6z M319,305.3h52.7c3.9-2.6,7.2-6,9.6-10c2.7-4.8,2.1-35,1.3-50.9&#10;&#9;&#9;h-33.8c0.2,5.6,1.4,41.6-3,54.3c-0.1,0.3-0.3,0.4-0.6,0.4h-21.1c-1.9,0-3.7,1.3-4.2,3.1L319,305.3z"/>\n\t<path class="st1_coding-2-31" d="M380.6,287.7c0,8.6-2.6,11.2-6,11.2h-13.5c-1.9,0-3.6,1.2-4.3,3l-1.5,4.1h20.8c5.3,0,9.1-8.1,9.3-16.7&#10;&#9;&#9;s0-45.5,0-45.5h-4.6C380.8,243.8,380.6,279.1,380.6,287.7z"/>\n\t<path class="st1_coding-2-31" d="M376.1,306.6h-20.8c-0.2,0-0.4-0.1-0.5-0.3c-0.1-0.2-0.1-0.4-0.1-0.6l1.5-4.1c0.8-2,2.7-3.4,4.9-3.4h13.5&#10;&#9;&#9;c1.3,0,5.4,0,5.4-10.5c0-8.5,0.2-43.6,0.2-43.9c0-0.4,0.3-0.6,0.6-0.6h4.6c0.4,0,0.6,0.3,0.6,0.6c0,0.4,0.2,37,0,45.5&#10;&#9;&#9;S382.1,306.6,376.1,306.6z M356.3,305.3h19.8c4.6,0,8.5-7.2,8.6-16c0.1-7.9,0-39.9,0-44.8h-3.3c0,4.9-0.2,35.4-0.2,43.3&#10;&#9;&#9;s-2.2,11.8-6.7,11.8h-13.5c-1.6,0-3.1,1-3.6,2.5L356.3,305.3z"/>\n\t<path class="st1_coding-2-31" d="M308.1,147.4l-8.1,93c-0.5,4,2.3,7.7,6.4,8.3c0.3,0,0.6,0.1,0.9,0.1h110.9c4.6-0.2,8.3-3.7,8.7-8.3l8.1-93&#10;&#9;&#9;c0.5-4-2.3-7.7-6.3-8.3c-0.3,0-0.6-0.1-0.9-0.1H316.8C312.2,139.3,308.4,142.8,308.1,147.4z"/>\n\t<path class="st1_coding-2-31" d="M418.1,249.4H307.2c-2.2,0-4.3-0.9-5.8-2.5c-1.6-1.8-2.4-4.1-2.1-6.5l8.1-93c0.4-4.9,4.5-8.7,9.4-8.9h110.9&#10;&#9;&#9;c2.2,0,4.3,0.9,5.8,2.5c1.6,1.8,2.4,4.1,2.1,6.5l-8.1,93C427,245.4,423,249.2,418.1,249.4z M316.8,139.7c-4.3,0.2-7.7,3.5-8.1,7.7&#10;&#9;&#9;l0,0l-8.1,93c-0.2,2,0.4,4,1.8,5.5c1.2,1.4,3,2.1,4.9,2.1h110.9c4.3-0.2,7.7-3.5,8.1-7.7l8.1-93c0.2-2-0.4-4-1.8-5.5&#10;&#9;&#9;c-1.2-1.4-3-2.1-4.9-2.1L316.8,139.7z M308.1,147.4L308.1,147.4z"/>\n\t<path class="st0_coding-2-31" d="M307.7,147l-7.8,88.8c-0.5,3.9,2.2,7.4,6,7.9c0.3,0,0.6,0.1,0.9,0.1h105.9c4.4-0.2,8-3.6,8.3-8l7.8-88.8&#10;&#9;&#9;c0.5-3.8-2.2-7.4-6-7.9c-0.3,0-0.7-0.1-1-0.1H316C311.6,139.2,308.1,142.6,307.7,147z"/>\n\t<path class="st1_coding-2-31" d="M412.7,244.4H306.9c-2.1,0-4.1-0.9-5.6-2.4c-1.5-1.7-2.2-4-2-6.2L307,147l0,0c0.4-4.7,4.3-8.4,9-8.5h105.9&#10;&#9;&#9;c2.1,0,4.1,0.9,5.6,2.4c1.5,1.7,2.2,4,2,6.2l-7.8,88.8C421.3,240.6,417.4,244.2,412.7,244.4z M308.3,147.1l-7.8,88.8&#10;&#9;&#9;c-0.2,1.9,0.4,3.8,1.7,5.2c1.2,1.3,2.9,2,4.6,2h105.9c4.1-0.1,7.4-3.3,7.7-7.4l7.8-88.8c0.2-1.9-0.4-3.8-1.7-5.2&#10;&#9;&#9;c-1.2-1.3-2.9-2-4.6-2H316C311.9,139.9,308.6,143.1,308.3,147.1L308.3,147.1z"/>\n\t<path class="st0_coding-2-31" d="M301.2,220.9l-1.3,14.9c-0.5,3.9,2.2,7.4,6,7.9c0.3,0,0.6,0.1,0.9,0.1h105.9c4.4-0.2,8-3.6,8.3-8l1.3-14.9&#10;&#9;&#9;H301.2z"/>\n\t<path class="st1_coding-2-31" d="M412.7,244.4H306.9c-2.1,0-4.1-0.9-5.6-2.4c-1.5-1.7-2.2-4-2-6.2l1.3-14.9c0-0.3,0.3-0.6,0.6-0.6h121.1&#10;&#9;&#9;c0.2,0,0.3,0.1,0.5,0.2c0.1,0.1,0.2,0.3,0.2,0.5l-1.3,14.9C421.3,240.6,417.5,244.2,412.7,244.4z M301.8,221.6l-1.2,14.3&#10;&#9;&#9;c-0.2,1.9,0.4,3.8,1.7,5.2c1.2,1.3,2.9,2,4.6,2h105.9c4.1-0.1,7.4-3.3,7.7-7.4l1.2-14.2H301.8z"/>\n\t\n\t\t<ellipse transform="matrix(0.5567 -0.8307 0.8307 0.5567 -33.0505 402.6997)" class="st0_coding-2-31" cx="360.8" cy="232.3" rx="5.3" ry="4.8"/>\n\t<path class="st1_coding-2-31" d="M360.4,238.1c-1.4,0-2.8-0.6-3.8-1.6c-1-1.1-1.5-2.7-1.4-4.2c0.3-3.2,2.9-5.6,6-5.7c1.4,0,2.8,0.6,3.8,1.6&#10;&#9;&#9;c1,1.2,1.5,2.7,1.4,4.2C366.1,235.6,363.5,238,360.4,238.1z M361.3,227.8c-2.5,0.1-4.5,2.1-4.8,4.6c-0.1,1.2,0.2,2.3,1,3.2&#10;&#9;&#9;c0.7,0.8,1.7,1.2,2.8,1.2c2.5-0.1,4.5-2.1,4.8-4.6c0.1-1.2-0.2-2.3-1-3.2C363.3,228.3,362.3,227.8,361.3,227.8z"/>\n\t<path class="st1_coding-2-31" d="M420.4,145H316.5c-2.3,0.1-4.1,1.9-4.3,4.1l-5.5,62.6c-0.3,2,1.1,3.8,3.1,4.1c0.2,0,0.3,0,0.5,0h103.8&#10;&#9;&#9;c2.3-0.1,4.1-1.9,4.3-4.1l5.5-62.6c0.3-2-1.1-3.8-3.1-4.1C420.7,145,420.5,145,420.4,145z"/>\n\t<path class="st0_coding-2-31" d="M333.9,152.7h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C334.5,152.4,334.2,152.7,333.9,152.7z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M357.1,152.7h-20.6c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h20.6c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C357.8,152.4,357.5,152.7,357.1,152.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M363.5,156.7h-20.6c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h20.6c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C364.2,156.4,363.9,156.7,363.5,156.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M335.6,156.7h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C336.2,156.4,335.9,156.7,335.6,156.7z"/>\n\t<path class="st0_coding-2-31" d="M337.3,160.8h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C337.9,160.5,337.6,160.8,337.3,160.8L337.3,160.8z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M366.5,160.8h-25.8c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h25.8c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C367.1,160.5,366.8,160.8,366.5,160.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M338.9,164.8h-10.3c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h10.3c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C339.6,164.5,339.3,164.8,338.9,164.8z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M371.1,164.8h-30.6c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6l0,0h30.6c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C371.7,164.5,371.4,164.8,371.1,164.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M335.5,168.8h-10.3c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6l0,0h10.3c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C336.1,168.5,335.8,168.8,335.5,168.8L335.5,168.8z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M354.2,168.8h-16.6c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h16.6c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C354.8,168.5,354.5,168.8,354.2,168.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M377.2,168.8h-16.6c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6l0,0h16.6c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C377.8,168.5,377.5,168.8,377.2,168.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M334.7,172.9h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C335.4,172.6,335.1,172.9,334.7,172.9z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M353.5,172.9h-14.5c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h14.5c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C354.1,172.6,353.8,172.9,353.5,172.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M361.8,172.9h-5.9c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h5.9c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C362.5,172.6,362.2,172.9,361.8,172.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M334,176.9h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7H334c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C334.6,176.6,334.4,176.9,334,176.9z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M357.9,176.9h-21.2c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h21.2c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C358.6,176.6,358.3,176.9,357.9,176.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M370.7,176.9h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C371.4,176.6,371.1,176.9,370.7,176.9L370.7,176.9z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M326,181h-5.5c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h5.5c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C326.6,180.7,326.4,181,326,181z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M354.4,181h-23.9c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h23.9c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C355.1,180.7,354.8,181,354.4,181z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M330.1,185h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C330.7,184.7,330.4,185,330.1,185L330.1,185z"/>\n\t<path class="st0_coding-2-31" d="M341.1,189h-20.6c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h20.6c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C341.8,188.7,341.5,189,341.1,189z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M358.9,189h-14.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h14.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C359.5,188.7,359.2,189,358.9,189z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M378.6,189h-17.7c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h17.7c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C379.3,188.7,379,189,378.6,189L378.6,189z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M350.7,193.1h-30c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h30c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C351.4,192.8,351.1,193.1,350.7,193.1z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M366.3,193.1h-13.5c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h13.5c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C366.9,192.8,366.6,193.1,366.3,193.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M408.7,193.1h-40.2c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h40.2c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C409.4,192.8,409.1,193.1,408.7,193.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M334,197.1h-14.2c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7H334c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C334.6,196.8,334.4,197.1,334,197.1z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M347.3,197.1h-10.5c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.5c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C348,196.8,347.7,197.1,347.3,197.1L347.3,197.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M360.6,197.1h-10.5c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.5c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C361.2,196.8,360.9,197.1,360.6,197.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M344.2,201.1h-25.1c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6l0,0h25.1c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C344.9,200.8,344.6,201.1,344.2,201.1z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M359.9,201.1h-12.6c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h12.5c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C360.5,200.8,360.2,201.1,359.9,201.1L359.9,201.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M382,201.1h-19.1c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6H382c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C382.7,200.8,382.4,201.1,382,201.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M403.2,201.1h-19.1c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h19.1c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C403.8,200.8,403.5,201.1,403.2,201.1z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M339.7,205.2h-15c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h15c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C340.3,204.9,340,205.2,339.7,205.2z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M357.5,205.2h-15c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h15c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C358.1,204.9,357.8,205.2,357.5,205.2z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M375.4,205.2h-15c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h15c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C376,204.9,375.7,205.2,375.4,205.2z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M393.8,205.6h-15c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6h15c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C394.5,205.3,394.2,205.6,393.8,205.6z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M336.5,209.2h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C337.2,208.9,336.9,209.2,336.5,209.2L336.5,209.2z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M349.3,209.2h-10.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h10.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C349.9,208.9,349.6,209.2,349.3,209.2z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M373,209.6L373,209.6l-21.2-0.4c-0.4,0-0.6-0.3-0.6-0.7c0,0,0,0,0,0c0-0.3,0.2-0.6,0.6-0.6c0,0,0.1,0,0.1,0&#10;&#9;&#9;l21.2,0.4c0.4,0,0.6,0.3,0.6,0.7C373.7,209.3,373.4,209.6,373,209.6L373,209.6z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M389.2,164.8h-14c-0.4,0-0.6-0.3-0.6-0.7c0-0.4,0.3-0.6,0.6-0.6l0,0h14c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;C389.9,164.5,389.6,164.8,389.2,164.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M399.5,164.8c-1.7,0.1-3.3,0-5-0.1c-0.3-0.1-0.6-0.4-0.5-0.8c0.1-0.3,0.4-0.6,0.8-0.5c0.7,0.1,9.8,0,15.8,0&#10;&#9;&#9;l0,0c0.4,0,0.6,0.3,0.6,0.6c0,0.4-0.3,0.6-0.6,0.6C405.4,164.8,401.9,164.8,399.5,164.8z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M388.5,156.7h-20.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h20.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C389.1,156.4,388.8,156.7,388.5,156.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M412.7,156.7h-20.2c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h20.2c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C413.3,156.4,413,156.7,412.7,156.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M370.6,152.7c-4.1,0-7,0-7.2,0c-0.4,0-0.6-0.4-0.6-0.7c0-0.3,0.4-0.6,0.7-0.6c0.7,0,17,0,23.3,0l0,0&#10;&#9;&#9;c0.4,0,0.6,0.3,0.6,0.6c0,0.4-0.3,0.7-0.6,0.7L370.6,152.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M392.4,152.7c-0.3,0-0.5-0.2-0.6-0.4c-0.1-0.3,0-0.7,0.3-0.9c0.1-0.1,0.4-0.2,14.1-0.1c0.4,0,0.6,0.3,0.6,0.6&#10;&#9;&#9;c0,0.4-0.3,0.6-0.6,0.6l0,0c-4.9-0.1-13-0.1-13.7,0L392.4,152.7z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M367.6,181h-10.5c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7l0,0h10.5c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C368.3,180.7,368,181,367.6,181z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M342.9,185h-7.7c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h7.7c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C343.6,184.7,343.3,185,342.9,185z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_coding-2-31" d="M364.1,185h-18.3c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h18.3c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C364.8,184.7,364.5,185,364.1,185z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M403.1,185h-35.4c-0.4,0-0.6-0.3-0.6-0.6c0-0.4,0.3-0.7,0.6-0.7h35.4c0.4,0,0.6,0.3,0.6,0.7&#10;&#9;&#9;C403.8,184.7,403.5,185,403.1,185z" style="fill: rgb(104, 225, 253);"/>\n</g>\n<g id="Mouse_coding-2-31">\n\t<path class="st1_coding-2-31" d="M336.7,306.2h36.6c0.7,0-4.2-15.8-16-16.2S336.7,306.2,336.7,306.2z"/>\n\t<path class="st1_coding-2-31" d="M373.4,306.8h-36.6c-0.4,0-0.7-0.3-0.7-0.7c0-0.1,0-0.2,0.1-0.3c0.4-0.7,9.2-17,21.3-16.6&#10;&#9;&#9;c11.5,0.4,16.7,14.9,16.7,16.7C374.1,306.4,373.8,306.8,373.4,306.8C373.4,306.8,373.4,306.8,373.4,306.8z M337.8,305.5h34.9&#10;&#9;&#9;c-0.6-2.9-5.7-14.5-15.4-14.9h-0.4C347.5,290.6,339.9,302.1,337.8,305.5L337.8,305.5z"/>\n</g>\n<g id="Keyboard_coding-2-31">\n\t<rect x="124.7" y="296.1" class="st0_coding-2-31" width="121.7" height="9.2"/>\n\t<path class="st1_coding-2-31" d="M246.4,306H124.7c-0.4,0-0.7-0.3-0.7-0.6v-9.2c0-0.4,0.3-0.6,0.7-0.6h121.7c0.4,0,0.6,0.3,0.6,0.6v9.2&#10;&#9;&#9;C247,305.7,246.8,306,246.4,306z M125.3,304.7h120.4v-7.9H125.3L125.3,304.7z"/>\n</g>\n<g id="Desk_coding-2-31">\n\t<rect x="60.5" y="322.2" class="st0_coding-2-31" width="27.2" height="64.7"/>\n\t<path class="st1_coding-2-31" d="M87.7,387.6H60.5c-0.4,0-0.6-0.3-0.7-0.6v-64.7c0-0.4,0.3-0.6,0.7-0.6h27.2c0.4,0,0.6,0.3,0.7,0.6V387&#10;&#9;&#9;C88.4,387.4,88.1,387.6,87.7,387.6z M61.1,386.3h25.9v-63.4H61.2L61.1,386.3z"/>\n\t<rect x="399.7" y="322.2" class="st0_coding-2-31" width="27.2" height="64.7"/>\n\t<path class="st1_coding-2-31" d="M427,387.6h-27.3c-0.4,0-0.6-0.3-0.6-0.6v-64.7c0-0.4,0.3-0.6,0.6-0.6H427c0.4,0,0.6,0.3,0.6,0.6V387&#10;&#9;&#9;C427.6,387.4,427.4,387.6,427,387.6z M400.4,386.3h25.9v-63.4h-26L400.4,386.3z"/>\n\t<rect x="60.5" y="322.2" class="st1_coding-2-31" width="27.2" height="16.8"/>\n\t<path class="st1_coding-2-31" d="M87.7,339.7H60.5c-0.4,0-0.6-0.3-0.7-0.6v-16.8c0-0.4,0.3-0.6,0.7-0.6h27.2c0.4,0,0.6,0.3,0.7,0.6V339&#10;&#9;&#9;C88.4,339.4,88.1,339.7,87.7,339.7C87.7,339.7,87.7,339.7,87.7,339.7z M61.1,338.4h25.9v-15.5H61.2L61.1,338.4z"/>\n\t<rect x="399.7" y="322.2" class="st1_coding-2-31" width="27.2" height="16.8"/>\n\t<path class="st1_coding-2-31" d="M427,339.7h-27.3c-0.4,0-0.6-0.3-0.6-0.6v-16.8c0-0.4,0.3-0.6,0.6-0.6H427c0.4,0,0.6,0.3,0.6,0.6V339&#10;&#9;&#9;C427.7,339.4,427.4,339.7,427,339.7C427,339.7,427,339.7,427,339.7z M400.4,338.4h25.9v-15.5h-26L400.4,338.4z"/>\n\t<rect x="43.9" y="306.1" class="st0_coding-2-31" width="399.7" height="16.2"/>\n\t<path class="st1_coding-2-31" d="M443.6,322.9H43.9c-0.4,0-0.6-0.3-0.7-0.6v-16.2c0-0.4,0.3-0.6,0.7-0.6h399.7c0.4,0,0.6,0.3,0.6,0.6v16.2&#10;&#9;&#9;C444.2,322.6,443.9,322.9,443.6,322.9C443.6,322.9,443.6,322.9,443.6,322.9z M44.6,321.6H443v-14.9H44.5L44.6,321.6z"/>\n</g>\n<g id="Character_coding-2-31">\n\t<path class="st1_coding-2-31" d="M199.4,331.5c0,0-58.6,14.1-60.4,24.4s2.8,30.6,2.8,30.6h151c0,0,7.2-42.7,0-58.9S199.4,331.5,199.4,331.5z"/>\n\t<path class="st1_coding-2-31" d="M292.8,387.2h-151c-0.3,0-0.6-0.2-0.6-0.5c-0.2-0.8-4.6-20.5-2.8-30.9c1.8-10.7,58.5-24.4,60.9-25l0,0&#10;&#9;&#9;c0.2,0,21.9-5.1,44.1-8c30.1-4,47-2.5,50.1,4.5c7.2,16.2,0.3,57.6,0,59.3C293.4,387,293.1,387.2,292.8,387.2z M142.3,385.9h150&#10;&#9;&#9;c0.8-5,6.5-43.1,0-58c-2.8-6.4-19.6-7.6-48.7-3.8c-22.1,2.9-43.6,7.9-44,8c-16.2,3.9-58.6,15.7-60,23.9&#10;&#9;&#9;C138,365.2,141.6,382.7,142.3,385.9L142.3,385.9z"/>\n\t<path class="st0_coding-2-31" d="M301,262.5l10.9,24.9c0,0,30.6,5.6,32.8,4.4s5.4-5.3,7.5-6.7s10.5-0.1,11.9,0.9s4.8,5.2,4.5,6.5&#10;&#9;&#9;s-2.4-0.1-2.4-0.1s3.1,2.1,2.4,3.7s-7.1-2.7-8.3-2.7s-4.5,9-8.1,12.1s-43.9,9-47.6,8.1s-24.6-31-24.6-31l4.2-19L301,262.5z"/>\n\t<path class="st1_coding-2-31" d="M305.8,314.4c-0.5,0-0.9,0-1.4-0.1c-3.9-0.9-22.8-28.1-25-31.2c-0.1-0.2-0.1-0.3-0.1-0.5l4.2-19&#10;&#9;&#9;c0.1-0.3,0.3-0.5,0.6-0.5l16.9-1.3c0.3,0,0.5,0.1,0.6,0.4l10.7,24.6c14.5,2.6,30.5,5.1,32,4.4c1.4-1,2.8-2.2,3.9-3.5&#10;&#9;&#9;c1.1-1.2,2.2-2.2,3.5-3.1c2.3-1.5,11.1-0.2,12.7,0.9c1.3,0.9,5.2,5.4,4.7,7.2c-0.1,0.4-0.4,0.7-0.7,0.9c0.7,0.7,1,1.7,0.7,2.7&#10;&#9;&#9;c-0.1,0.3-0.4,0.6-0.7,0.7c-1.1,0.4-3-0.5-5.8-1.8c-0.8-0.4-1.6-0.8-2.4-1.1c-0.8,1.1-1.5,2.3-2.1,3.6c-1.5,2.9-3.5,6.5-5.6,8.4&#10;&#9;&#9;c-2.4,2.1-17.6,4.7-24.1,5.7C319.8,313.2,309.7,314.4,305.8,314.4z M280.6,282.6c8,11.6,21.5,29.9,24,30.5c3.9,0.9,43.8-5.2,47-8&#10;&#9;&#9;c1.9-1.7,3.8-5.2,5.3-8c1.7-3.2,2.3-4.3,3.2-4.3c1.1,0.2,2.1,0.6,3.1,1.2c1.3,0.7,4.1,2,4.7,1.8c0.2-0.7-1.1-2-2.1-2.8l-0.1-0.1&#10;&#9;&#9;c-0.3-0.2-0.3-0.6-0.1-0.9c0.2-0.3,0.6-0.3,0.9-0.1l0.1,0.1c0.4,0.3,0.8,0.5,1.3,0.5c0.2-0.9-2.6-4.7-4.2-5.9&#10;&#9;&#9;c-1.2-0.9-9.4-2.1-11.2-0.9c-1.2,0.9-2.3,1.9-3.3,3c-1.3,1.4-2.7,2.7-4.2,3.7c-2.3,1.2-28.1-3.4-33.2-4.3c-0.2,0-0.4-0.2-0.5-0.4&#10;&#9;&#9;l-10.6-24.5l-15.9,1.2L280.6,282.6z"/>\n\t<path class="st0_coding-2-31" d="M174.9,264.4l-7.8,19.1c0,0-23.3-13.3-29.5-14.2c-17.6-2.7-24.1,8.6-24.4,10.5s17-0.1,17-0.1s-7.3,2.6-6.7,5.8&#10;&#9;&#9;c0.4,1.8,8.6-2.5,9.9-2.1s36.6,27.7,49,30.4s41-59.6,41-59.6"/>\n\t<path class="st1_coding-2-31" d="M183.2,314.5c-0.3,0-0.6,0-0.9-0.1c-9.8-2.1-32.9-18.8-44-26.8c-2.6-1.9-4.8-3.5-5.2-3.6&#10;&#9;&#9;c-1.3,0.2-2.5,0.6-3.7,1.1c-3.2,1.1-5.1,1.8-6.1,1.2c-0.3-0.2-0.5-0.4-0.6-0.8c-0.4-2,1.5-3.7,3.5-4.8c-5.3,0.5-12.4,1-13.6-0.2&#10;&#9;&#9;c-0.2-0.2-0.3-0.5-0.3-0.8c0.3-1.8,6.8-13.8,25.2-11c5.8,0.9,25.2,11.7,29.1,13.9l7.5-18.4c0.1-0.3,0.5-0.5,0.8-0.4c0,0,0,0,0,0&#10;&#9;&#9;c0.3,0.1,0.5,0.5,0.4,0.8c0,0,0,0,0,0l-7.8,19.1c-0.1,0.2-0.2,0.3-0.4,0.4c-0.2,0.1-0.4,0-0.5,0c-0.2-0.1-23.3-13.2-29.3-14.1&#10;&#9;&#9;c-17.4-2.6-22.9,8.2-23.6,9.8c1.5,0.6,9.4,0.1,16.2-0.7c0.4,0,0.7,0.2,0.7,0.6c0,0.3-0.1,0.6-0.4,0.7c-1.7,0.6-6.5,2.8-6.2,4.9&#10;&#9;&#9;c0.7,0.2,3.5-0.8,5-1.4c2.5-0.9,3.8-1.4,4.5-1.1c0.4,0.1,1.4,0.8,5.5,3.8c10.2,7.3,34,24.5,43.5,26.6c9.8,2.1,32.4-42,40.3-59.2&#10;&#9;&#9;c0.2-0.3,0.5-0.5,0.9-0.3c0.3,0.2,0.5,0.5,0.3,0.9C222.9,256.9,196.4,314.5,183.2,314.5z"/>\n\t<path class="st0_coding-2-31" d="M250.9,179.8c1.4-0.5,2.7-1.4,3.8-2.4c1.5-1.6,2.7-3.4,3.6-5.4c4.6-10.2,6.1-21.6,4.4-32.7&#10;&#9;&#9;c-0.7-4.8-1.7-11.4-4.5-15.5c-1.4-1.8-3.3-3.1-5.4-3.8c-0.6-0.2-6.7,0.2-6.1,0.9c-4.6-5.3-11.4-8.3-18.5-8&#10;&#9;&#9;c-5.9,0.2-13,2.8-16.8,7.5c-1.6,1.9-2.1,3.4-4.6,4.3c-3.3,1.1-6.9,0.9-10.1-0.5c-0.8-0.3-5.9-2.1-5.8-2.8&#10;&#9;&#9;c-0.2,6.9,3.7,13.3,9.9,16.3c-3.6,0.2-7.3-0.3-10.6-1.7c3.3,7.6,11.2,12.1,19.4,11.1c2.6,3.7,6,6.8,8.6,10.7&#10;&#9;&#9;c2.7,4.1,5.3,8.4,8.9,11.9C232.6,175.3,242.8,182.9,250.9,179.8z"/>\n\t<path class="st1_coding-2-31" d="M246.9,181.2c-8.1,0-16.7-7.3-20.4-10.8c-3.1-3.2-5.7-6.7-8-10.5l-1-1.5c-1.4-2-3-4-4.6-5.9&#10;&#9;&#9;c-1.3-1.4-2.6-2.9-3.7-4.5c-8.4,0.8-16.3-3.8-19.6-11.5c-0.1-0.2,0-0.5,0.1-0.7c0.2-0.2,0.5-0.2,0.7-0.1c2.6,1,5.3,1.6,8,1.7&#10;&#9;&#9;c-5.2-3.5-8.3-9.4-8.1-15.7c0-0.3,0.3-0.6,0.6-0.6c0,0,0,0,0,0c0.3,0,0.5,0.2,0.6,0.5c1.5,0.9,3,1.6,4.7,2.1l0.8,0.3&#10;&#9;&#9;c3,1.3,6.5,1.5,9.6,0.5c1.4-0.5,2.6-1.5,3.4-2.9c0.3-0.4,0.6-0.8,0.9-1.2c4.1-5,11.6-7.5,17.3-7.7c7-0.3,13.7,2.5,18.5,7.6&#10;&#9;&#9;c2-0.5,4.1-0.7,6.2-0.6c2.3,0.7,4.3,2.1,5.8,4c3,4.2,3.9,10.9,4.6,15.7c1.7,11.2,0.1,22.7-4.5,33.1c-0.9,2.1-2.1,4-3.7,5.6&#10;&#9;&#9;c-1.2,1.1-2.5,2-4,2.6l0,0C249.8,180.9,248.4,181.2,246.9,181.2z M209.4,146.6c0.2,0,0.4,0.1,0.5,0.3c1.2,1.6,2.5,3.2,3.9,4.8&#10;&#9;&#9;c1.7,1.9,3.3,3.9,4.7,6l1,1.5c2.2,3.7,4.8,7.2,7.9,10.3c4.2,4,14.9,13,23.3,9.8l0,0c1.3-0.5,2.5-1.3,3.6-2.3&#10;&#9;&#9;c1.4-1.5,2.6-3.3,3.4-5.2c4.5-10.1,6-21.3,4.4-32.3c-0.7-4.8-1.6-11.3-4.4-15.2c-1.3-1.7-3-2.9-5.1-3.5c-1.8,0-3.6,0.1-5.3,0.5&#10;&#9;&#9;c0,0.1-0.1,0.2-0.2,0.3c-0.3,0.2-0.7,0.2-0.9-0.1c0,0,0,0,0,0l0,0c-4.5-5.2-11.1-8-17.9-7.7c-5.4,0.2-12.5,2.5-16.3,7.2&#10;&#9;&#9;c-0.3,0.4-0.6,0.8-0.9,1.2c-0.9,1.5-2.3,2.7-4,3.3c-3.5,1.2-7.2,1-10.6-0.5l-0.8-0.3c-1.4-0.5-2.8-1.1-4.2-1.8&#10;&#9;&#9;c0.3,6.2,4,11.7,9.5,14.4c0.3,0.1,0.4,0.4,0.4,0.7c-0.1,0.3-0.3,0.5-0.6,0.5c-3.2,0.2-6.4-0.2-9.4-1.2&#10;&#9;&#9;C194.9,143.8,202,147.5,209.4,146.6L209.4,146.6z M191.5,121.6L191.5,121.6z"/>\n\t<path class="st0_coding-2-31" d="M208.8,160.9c0,0-6.8,13.1-4.8,15.5s7.3,0.1,7.3,0.1"/>\n\t<path class="st1_coding-2-31" d="M206.9,178.1c-1.3,0.1-2.5-0.4-3.4-1.3c-2.1-2.6,3.6-13.9,4.7-16.2c0.2-0.3,0.6-0.4,0.9-0.3s0.4,0.6,0.3,0.9&#10;&#9;&#9;l0,0c-3.2,6.3-5.9,13.5-4.9,14.8c1.4,1.6,5.2,0.5,6.6-0.1c0.3-0.1,0.7,0,0.9,0.3s0,0.7-0.3,0.9C210.1,177.7,208.5,178,206.9,178.1z&#10;&#9;&#9;"/>\n\t<path class="st0_coding-2-31" d="M208.8,144.5c-4.7,4.8-2.2,13.5-1.6,19.3c0.9,8.1,2.1,16.2,3.4,24.3c0.8,5.1,14.2,3.8,16.4,2l0.1,20.6&#10;&#9;&#9;l28.5-4.8l-4.6-25.7c0,0-9.1,1.1-15.4-8.9s-8.1-32.9-8.1-32.9S213.4,139.9,208.8,144.5z"/>\n\t<path class="st1_coding-2-31" d="M227.2,211.3c-0.2,0-0.3-0.1-0.4-0.2c-0.1-0.1-0.2-0.3-0.2-0.5l-0.1-19.5c-2.9,1.2-9.4,1.8-13.2,0.3&#10;&#9;&#9;c-2.3-0.9-3-2.3-3.2-3.3c-1.3-8.1-2.5-16.2-3.4-24.4c-0.1-1-0.3-2-0.4-3.1c-0.9-5.6-1.9-12.5,2.2-16.7c4.7-4.8,18.5-6.2,19.1-6.3&#10;&#9;&#9;c0.2,0,0.3,0,0.5,0.1c0.1,0.1,0.2,0.3,0.2,0.4c0,0.2,1.8,22.9,8,32.6c6.1,9.5,14.5,8.6,14.8,8.6c0.3,0,0.7,0.2,0.7,0.5l4.6,25.7&#10;&#9;&#9;c0,0.2,0,0.3-0.1,0.5c-0.1,0.1-0.3,0.2-0.4,0.3L227.2,211.3L227.2,211.3z M227,189.4c0.4,0,0.6,0.3,0.6,0.6c0,0,0,0,0,0l0.1,19.8&#10;&#9;&#9;l27.1-4.6l-4.4-24.5c-2.2,0.1-9.8-0.4-15.5-9.2c-5.9-9.1-7.8-28.5-8.2-32.5c-2.8,0.4-13.9,2-17.7,5.8c-3.7,3.7-2.6,10.3-1.8,15.6&#10;&#9;&#9;c0.2,1.1,0.3,2.2,0.5,3.2c0.9,8.1,2.1,16.3,3.4,24.3c0.2,1,0.9,1.8,2.4,2.3c4.1,1.5,11.6,0.5,13-0.7&#10;&#9;&#9;C226.7,189.5,226.9,189.4,227,189.4z"/>\n\t<path class="st0_coding-2-31" d="M210.2,182c0,0,6.7,3.2,9.4-3.7"/>\n\t<path class="st1_coding-2-31" d="M213.6,183.4c-1.3,0-2.6-0.3-3.7-0.8c-0.3-0.2-0.4-0.6-0.2-0.9c0.2-0.3,0.5-0.4,0.8-0.3&#10;&#9;&#9;c1.7,0.7,3.5,0.8,5.3,0.3c1.5-0.7,2.7-2,3.2-3.6c0.1-0.3,0.5-0.5,0.8-0.4s0.5,0.5,0.4,0.8c0,0,0,0,0,0.1c-0.6,2-2.1,3.6-4,4.4&#10;&#9;&#9;C215.3,183.2,214.5,183.4,213.6,183.4z"/>\n\t<path class="st0_coding-2-31" d="M225,164.4c-0.2-2,0.8-4,1.7-5.8c0.6-1.5,1.5-2.8,2.6-4c1.1-1.2,2.6-1.9,4.2-1.8c1.4,0.2,2.7,1,3.5,2.2&#10;&#9;&#9;c0.8,1.2,1.3,2.5,1.5,3.9c0.9,6.2-1.5,12.4-6.4,16.4l0.4-0.5"/>\n\t<path class="st1_coding-2-31" d="M232,175.9c-0.4,0-0.6-0.3-0.6-0.7c0-0.1,0-0.2,0.1-0.3l0.4-0.5c0.1-0.2,0.3-0.3,0.5-0.3l0,0&#10;&#9;&#9;c4.2-3.8,6.2-9.5,5.3-15.1c-0.2-1.3-0.6-2.6-1.4-3.7c-0.7-1-1.8-1.7-3-1.9c-1.4,0-2.8,0.5-3.7,1.6c-1,1.2-1.8,2.4-2.4,3.9&#10;&#9;&#9;c-0.8,1.6-1.8,3.6-1.6,5.5c0,0.4-0.2,0.7-0.6,0.7c0,0,0,0,0,0c-0.4,0-0.7-0.2-0.7-0.6c-0.2-2.3,0.9-4.4,1.7-6.2&#10;&#9;&#9;c0.7-1.5,1.6-2.9,2.7-4.2c1.2-1.4,3-2.1,4.8-2c1.6,0.2,3,1.1,3.9,2.4c0.8,1.3,1.4,2.7,1.6,4.2c1,6.4-1.5,12.9-6.6,17&#10;&#9;&#9;C232.3,175.8,232.1,175.9,232,175.9z"/>\n\t\n\t\t<ellipse transform="matrix(0.9985 -5.460164e-02 5.460164e-02 0.9985 -8.1102 11.7244)" class="st1_coding-2-31" cx="210.5" cy="154.3" rx="1.1" ry="2.9"/>\n\t<path class="st1_coding-2-31" d="M227,190.1c4.7-0.4,9.2-1.8,13.4-4.1c0,0-2.7,12.6-12.8,14.3L227,190.1z"/>\n\t<path class="st1_coding-2-31" d="M227.5,200.9c-0.2,0-0.3-0.1-0.4-0.1c-0.1-0.1-0.2-0.3-0.2-0.5l-0.5-10.1c0-0.4,0.3-0.7,0.6-0.7&#10;&#9;&#9;c4.6-0.4,9-1.8,13-4c0.3-0.2,0.7-0.1,0.9,0.2c0.1,0.2,0.1,0.3,0.1,0.5c-0.1,0.5-2.9,13.1-13.4,14.8L227.5,200.9z M227.7,190.7&#10;&#9;&#9;l0.4,8.8c7.1-1.6,10.2-9,11.2-12.2C235.7,189.1,231.7,190.2,227.7,190.7L227.7,190.7z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M297.7,331.5c0,0-1.4-95.1-15.7-117.1s-51.2-26.8-69-13.8s-13.7,130.8-13.7,130.8H297.7z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st2_coding-2-31 targetColor" d="M225.4,195c0,0-21.1,1.8-33.4,11.9s-24.9,61.9-24.9,61.9l38.9,8.8L225.4,195z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st1_coding-2-31" d="M200.4,298.6L200.4,298.6c-0.4,0-0.6-0.3-0.6-0.7c0,0,0,0,0,0c0.5-28,1.3-75,1.6-75.8c0.1-0.3,0.5-0.5,0.9-0.3&#10;&#9;&#9;c0.3,0.1,0.5,0.5,0.4,0.8c-0.3,2-1.1,50.1-1.6,75.3C201,298.4,200.8,298.7,200.4,298.6z"/>\n\t<path class="st2_coding-2-31 targetColor" d="M267.4,201c0,0,17.8,2,27.2,21.6c5.1,10.6,18.2,44.8,18.2,44.8l-39.3,4.5L267.4,201z" style="fill: rgb(104, 225, 253);"/>\n</g>\n<g id="Cup_coding-2-31">\n\t<path class="st3_coding-2-31" d="M84.1,297.1l-4.9-0.1c-0.4,0-0.7-0.3-0.7-0.6s0.3-0.7,0.6-0.7c0,0,0,0,0,0l4.9,0.2c2.5,0.2,4.6-1.7,4.8-4.2&#10;&#9;&#9;s-1.7-4.6-4.2-4.8c-0.1,0-0.2,0-0.3,0c-0.4,0-0.7-0.3-0.7-0.6s0.3-0.7,0.6-0.7c0,0,0,0,0,0c3.2,0.2,5.6,2.9,5.4,6.1&#10;&#9;&#9;C89.6,294.8,87.1,297.2,84.1,297.1L84.1,297.1z"/>\n\t<path class="st0_coding-2-31" d="M93.4,300c-0.1,3.2-10.9,5.4-24.1,4.9s-23.8-3.3-23.8-6.5L93.4,300z"/>\n\t<path class="st3_coding-2-31" d="M69.2,305.6c-11.9-0.4-24.5-3-24.4-7.2c0-0.4,0.3-0.6,0.7-0.6l47.9,1.6c0.4,0,0.6,0.3,0.6,0.7c0,0,0,0,0,0&#10;&#9;&#9;C93.9,304.2,81.2,306,69.2,305.6z M46.4,299.2c1.5,2.1,9.9,4.8,22.9,5.2s21.5-1.7,23.2-3.7L46.4,299.2z"/>\n\t<polygon class="st0_coding-2-31" points="81.7,299.7 57.2,298.9 53.1,280.4 87,281.5 &#9;"/>\n\t<path class="st3_coding-2-31" d="M81.7,300.3l-24.5-0.8c-0.3,0-0.6-0.2-0.6-0.5l-4.1-18.5c0-0.2,0-0.4,0.1-0.6c0.1-0.2,0.3-0.2,0.5-0.2&#10;&#9;&#9;l33.9,1.1c0.2,0,0.4,0.1,0.5,0.3c0.1,0.2,0.2,0.4,0.1,0.6l-5.3,18.1C82.2,300.1,82,300.3,81.7,300.3z M57.7,298.2l23.5,0.8&#10;&#9;&#9;l4.9-16.9l-32.2-1.1L57.7,298.2z"/>\n</g>\n<g id="Books_coding-2-31">\n\t<rect x="388.6" y="295.8" class="st0_coding-2-31" width="52.4" height="9.2"/>\n\t<path class="st3_coding-2-31" d="M441.1,305.7h-52.4c-0.4,0-0.7-0.3-0.7-0.6c0,0,0,0,0,0v-9.2c0-0.4,0.3-0.6,0.6-0.6h52.4&#10;&#9;&#9;c0.4,0,0.6,0.3,0.6,0.6v9.2C441.7,305.4,441.4,305.7,441.1,305.7C441.1,305.7,441.1,305.7,441.1,305.7z M389.3,304.4h51.1v-7.9&#10;&#9;&#9;h-51.1V304.4z"/>\n\t<rect x="396" y="286.6" class="st0_coding-2-31" width="60.1" height="9.2"/>\n\t<path class="st3_coding-2-31" d="M456.1,296.5H396c-0.4,0-0.6-0.3-0.6-0.6v-9.2c0-0.4,0.3-0.6,0.6-0.6h60.1c0.4,0,0.6,0.3,0.6,0.6v9.2&#10;&#9;&#9;C456.8,296.2,456.5,296.5,456.1,296.5C456.1,296.5,456.1,296.5,456.1,296.5z M396.6,295.2h58.8v-7.9h-58.8L396.6,295.2z"/>\n\t<rect x="390.6" y="277.4" class="st0_coding-2-31" width="60.1" height="9.2"/>\n\t<path class="st3_coding-2-31" d="M450.7,287.2h-60.1c-0.4,0-0.6-0.3-0.6-0.6v-9.2c0-0.4,0.3-0.6,0.6-0.6h60.1c0.4,0,0.6,0.3,0.6,0.6v9.2&#10;&#9;&#9;C451.4,286.9,451.1,287.2,450.7,287.2z M391.3,285.9h58.8V278h-58.8L391.3,285.9z"/>\n\t<rect x="420.7" y="295.8" class="st1_coding-2-31" width="27.5" height="9.2"/>\n\t<path class="st1_coding-2-31" d="M448.2,305.7h-27.5c-0.4,0-0.7-0.3-0.7-0.6c0,0,0,0,0,0v-9.2c0-0.4,0.3-0.6,0.6-0.6h27.5&#10;&#9;&#9;c0.4,0,0.6,0.3,0.6,0.6v9.2C448.9,305.4,448.6,305.6,448.2,305.7z M421.3,304.4h26.2v-7.9h-26.2V304.4z"/>\n\t<rect x="424.5" y="286.6" class="st1_coding-2-31" width="31.6" height="9.2"/>\n\t<path class="st1_coding-2-31" d="M456.1,296.5h-31.6c-0.4,0-0.6-0.3-0.6-0.6v-9.2c0-0.4,0.3-0.6,0.6-0.6h31.6c0.4,0,0.6,0.3,0.6,0.6v9.2&#10;&#9;&#9;C456.8,296.2,456.5,296.5,456.1,296.5z M425.2,295.2h30.3v-7.9h-30.3L425.2,295.2z"/>\n\t<rect x="421.7" y="277.4" class="st1_coding-2-31" width="31.6" height="9.2"/>\n\t<path class="st1_coding-2-31" d="M453.3,287.2h-31.6c-0.4,0-0.6-0.3-0.6-0.6v-9.2c0-0.4,0.3-0.6,0.6-0.6h31.6c0.4,0,0.6,0.3,0.6,0.6v9.2&#10;&#9;&#9;C453.9,286.9,453.6,287.2,453.3,287.2z M422.4,285.9h30.3V278h-30.3V285.9z"/>\n</g>\n<g id="Chair_coding-2-31">\n\t<path class="st1_coding-2-31" d="M302.3,305.3h-61.9c-7.6,0-13.7-6.1-13.7-13.7c0-0.6,0-1.2,0.1-1.8l6.8-52.1c0.9-6.8,6.7-11.9,13.6-11.9h61.9&#10;&#9;&#9;c7.6,0,13.7,6.2,13.7,13.7c0,0.6,0,1.2-0.1,1.8l-6.8,52.1C315,300.2,309.2,305.3,302.3,305.3z"/>\n\t<path class="st1_coding-2-31" d="M302.3,306h-61.9c-7.9,0-14.4-6.4-14.4-14.4c0-0.6,0-1.2,0.1-1.9l6.8-52.1c0.9-7.2,7-12.5,14.2-12.5h61.9&#10;&#9;&#9;c7.9,0,14.4,6.4,14.4,14.4c0,0.6,0,1.3-0.1,1.9l-6.8,52.1C315.6,300.6,309.5,306,302.3,306z M247.2,226.5c-6.6,0-12.1,4.9-13,11.4&#10;&#9;&#9;l-6.8,52.1c-0.9,7.2,4.1,13.7,11.2,14.6c0.6,0.1,1.2,0.1,1.8,0.1h61.9c6.6,0,12.1-4.9,13-11.4l6.8-52.1c0.9-7.2-4.1-13.7-11.3-14.7&#10;&#9;&#9;c-0.6-0.1-1.1-0.1-1.7-0.1L247.2,226.5z"/>\n\t<path class="st1_coding-2-31" d="M262.6,271.9c0,0,7.4,8.7,7.7,11.9s-14.6,77.9-14.6,77.9l21.1-5.9c0,0,14.6-69.6,13.2-74.9&#10;&#9;&#9;s-10.1-12.1-10.1-12.1L262.6,271.9z"/>\n\t<path class="st1_coding-2-31" d="M255.7,362.3c-0.4,0-0.7-0.3-0.7-0.6c0,0,0-0.1,0-0.1c6-30,14.8-75.4,14.6-77.7c-0.2-2.5-5.5-9.2-7.5-11.6&#10;&#9;&#9;c-0.2-0.3-0.2-0.7,0.1-0.9c0.1-0.1,0.2-0.1,0.3-0.1l17.3-3.2c0.2,0,0.4,0,0.5,0.1c0.4,0.3,8.9,7,10.4,12.5S278,353,277.4,355.9&#10;&#9;&#9;c0,0.2-0.2,0.4-0.5,0.5l-21.1,5.9L255.7,362.3z M263.8,272.3c2,2.4,6.9,8.6,7.1,11.4c0.3,3.1-12.6,67.6-14.4,77l19.7-5.5&#10;&#9;&#9;c4.1-19.6,14.3-70,13.2-74.2c-1.2-4.6-8.3-10.5-9.7-11.6L263.8,272.3z"/>\n\t<path class="st1_coding-2-31" d="M191.3,353.2H299c4.9,0,8.8,3.9,8.8,8.8v15.7c0,4.9-3.9,8.8-8.8,8.8H191.3c-4.9,0-8.8-3.9-8.8-8.8V362&#10;&#9;&#9;C182.5,357.2,186.4,353.2,191.3,353.2z"/>\n\t<path class="st1_coding-2-31" d="M299,387.2H191.3c-5.2,0-9.4-4.2-9.4-9.4V362c0-5.2,4.2-9.4,9.4-9.4H299c5.2,0,9.4,4.2,9.4,9.4v15.7&#10;&#9;&#9;C308.4,383,304.2,387.2,299,387.2L299,387.2z M191.3,353.9c-4.5,0-8.1,3.7-8.1,8.1v15.7c0,4.5,3.6,8.1,8.1,8.1H299&#10;&#9;&#9;c4.5,0,8.1-3.6,8.1-8.1V362c0-4.5-3.6-8.1-8.1-8.1L191.3,353.9z"/>\n\t<path class="st0_coding-2-31" d="M182.4,379.6c-0.4,0-0.6-0.3-0.6-0.6v-16.6c0-5.5,4.4-9.9,9.8-10l65.4-1.1l11.6-59.7c0-0.1,2.8-13.5-4.7-17.2&#10;&#9;&#9;c-0.3-0.2-0.4-0.5-0.3-0.9c0,0,0,0,0,0c0.1-0.3,0.5-0.5,0.8-0.3c0,0,0,0,0,0c8.4,4.1,5.5,18,5.4,18.6l-11.7,60.2&#10;&#9;&#9;c-0.1,0.3-0.3,0.5-0.6,0.5l-66,1.1c-4.7,0.1-8.5,4-8.6,8.7V379C183,379.3,182.8,379.6,182.4,379.6z"/>\n\t<path class="st0_coding-2-31" d="M290,283.6L290,283.6c-0.4,0-0.6-0.3-0.6-0.7c0,0,0,0,0,0c0.3-4.1-1.7-7.9-5.2-10c-0.3-0.2-0.4-0.6-0.2-0.9&#10;&#9;&#9;c0.2-0.3,0.6-0.4,0.9-0.2c3.9,2.4,6.1,6.7,5.8,11.2C290.7,283.4,290.4,283.6,290,283.6C290,283.6,290,283.6,290,283.6z"/>\n\t<path class="st0_coding-2-31" d="M299.2,353.9L299.2,353.9l-21.8-0.2c-0.2,0-0.4-0.1-0.5-0.2c-0.1-0.1-0.2-0.3-0.1-0.5l4.4-21.6&#10;&#9;&#9;c0.1-0.3,0.4-0.6,0.8-0.5c0.3,0.1,0.6,0.4,0.5,0.8l-4.2,20.9l21,0.1c0.4,0,0.6,0.3,0.6,0.7C299.8,353.6,299.5,353.9,299.2,353.9z"/>\n</g>\n</svg>
7	t	2025-08-10 12:33:40.39305+00	2025-09-13 11:38:09.230391+00	Physique-Chimie	3	Explorez les lois qui gouvernent le monde	#FF5722	<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 500 500" style="width: 175px;" xml:space="preserve" data-imageid="science-1-42" imageName="Science 1" class="illustrations_image">\n<style type="text/css">\n\t.st0_science-1-42{fill:#093F68;}\n\t.st1_science-1-42{fill:#68E1FD;}\n\t.st2_science-1-42{fill:#FFFFFF;}\n\t.st3_science-1-42{fill:#FFBC0E;}\n\t.st4_science-1-42{fill:#F56132;}\n\t.st5_science-1-42{fill:#70CC40;}\n\t.st6_science-1-42{fill:#DFEAEF;}\n\t.st7_science-1-42{fill:#FFC9B0;}\n\t.st8_science-1-42{fill:#725858;}\n</style>\n<g id="light_science-1-42">\n\t<circle class="st0_science-1-42" cx="348.6" cy="300.4" r="32.5"/>\n\t<path class="st0_science-1-42" d="M348.6,334.3c-18.8,0-34-15.2-34-34s15.2-34,34-34s34,15.2,34,34l0,0c0,18.7-15.1,34-33.8,34&#10;&#9;&#9;C348.7,334.3,348.7,334.3,348.6,334.3z M348.6,269.5c-17,0-30.9,13.8-30.9,30.9s13.8,30.9,30.9,30.9s30.9-13.8,30.9-30.9&#10;&#9;&#9;c0,0,0,0,0,0l0,0C379.5,283.3,365.7,269.5,348.6,269.5C348.6,269.5,348.6,269.5,348.6,269.5z"/>\n\t<path class="st1_science-1-42 targetColor" d="M422.5,165.6c0-40.3-32.6-72.9-72.8-72.9c0,0-0.1,0-0.1,0c-1.7,0-3.5,0.1-5.1,0.2c-36,2.5-65.2,31.7-67.6,67.7&#10;&#9;&#9;c-1.2,17.6,3.9,35,14.6,49.1c14.1,18.6,21.8,41.3,21.8,64.7h72.6c0-23,7.1-45.7,21.2-63.9C417.1,197.6,422.6,181.9,422.5,165.6z" style="fill: rgb(104, 225, 253);"/>\n\t<path class="st0_science-1-42" d="M386,275.8h-72.7c-0.8,0-1.5-0.7-1.5-1.5c0,0,0,0,0,0c-0.1-23-7.6-45.4-21.5-63.7&#10;&#9;&#9;c-24.8-32.8-18.4-79.5,14.4-104.3s79.5-18.4,104.3,14.4c9.8,12.9,15.1,28.7,15.1,44.9c0.1,16.6-5.4,32.7-15.7,45.7&#10;&#9;&#9;c-13.5,17.3-20.9,39.6-20.9,63C387.5,275.2,386.8,275.8,386,275.8C386,275.9,386,275.9,386,275.8L386,275.8z M314.8,272.8h69.6&#10;&#9;&#9;c0.3-23.4,7.9-45.9,21.6-63.3c9.8-12.5,15.1-28,15-43.8c-0.1-39.4-32.1-71.3-71.5-71.2s-71.3,32.1-71.2,71.5&#10;&#9;&#9;c0,15.4,5.1,30.4,14.3,42.8C306.7,227.2,314.4,249.6,314.8,272.8L314.8,272.8z"/>\n\t<path class="st2_science-1-42" d="M309.1,294.5h79.1c2.5,0,4.6,2.1,4.6,4.6v11c0,2.6-2.1,4.6-4.6,4.6h-79.1c-2.6,0-4.6-2.1-4.6-4.6v-11&#10;&#9;&#9;C304.5,296.6,306.5,294.6,309.1,294.5z"/>\n\t<path class="st0_science-1-42" d="M384.3,316.3h-71.4c-5.5-0.1-9.9-4.5-10-10V303c0-5.5,4.5-10,10-10h71.4c5.5,0,10,4.5,10,10v3.3&#10;&#9;&#9;C394.3,311.8,389.9,316.3,384.3,316.3z M312.9,296.1c-3.8,0-6.9,3.1-6.9,6.9l0,0v3.3c0,3.8,3.1,6.9,6.9,6.9h71.4&#10;&#9;&#9;c3.8,0,6.9-3.1,6.9-6.9v-3.3c0-3.8-3.1-6.9-6.9-6.9H312.9z"/>\n\t<path class="st2_science-1-42" d="M309.1,274.4h79.1c2.6,0,4.6,2.1,4.6,4.6v11c0,2.5-2.1,4.6-4.6,4.6h-79.1c-2.5,0-4.6-2.1-4.6-4.6v-11&#10;&#9;&#9;C304.5,276.5,306.5,274.4,309.1,274.4z"/>\n\t<path class="st0_science-1-42" d="M384.3,296.1h-71.4c-5.5-0.1-9.9-4.5-10-10v-3.3c0.1-5.5,4.5-9.9,10-10h71.4c5.5,0,10,4.5,10,10v3.3&#10;&#9;&#9;C394.3,291.7,389.9,296.1,384.3,296.1z M312.9,275.9c-3.8,0-6.9,3.1-6.9,6.9l0,0v3.3c0,3.8,3.1,6.9,6.9,6.9h71.4&#10;&#9;&#9;c3.8,0,6.9-3.1,6.9-6.9v-3.3c0-3.8-3.1-6.9-6.9-6.9H312.9z"/>\n\t<path class="st2_science-1-42" d="M309.1,254.2h79.1c2.6,0,4.6,2.1,4.6,4.6v11c0,2.5-2.1,4.6-4.6,4.6h-79.1c-2.6,0-4.6-2.1-4.6-4.6v-11&#10;&#9;&#9;C304.4,256.3,306.5,254.3,309.1,254.2z"/>\n\t<path class="st0_science-1-42" d="M384.3,275.9h-71.4c-5.5-0.1-9.9-4.5-10-10v-3.2c0-5.5,4.5-10,10-10h71.4c5.5,0,10,4.5,10,10v3.3&#10;&#9;&#9;C394.3,271.5,389.8,275.9,384.3,275.9z M312.9,255.8c-3.8,0-6.9,3.1-6.9,6.9v3.3c0,3.8,3.1,6.9,6.9,6.9h71.4c3.8,0,6.9-3.1,6.9-6.9&#10;&#9;&#9;v-3.3c0-3.8-3.1-6.9-6.9-6.9L312.9,255.8z"/>\n\t<path class="st2_science-1-42" d="M330.3,249.4c-0.7,0-1.4-0.5-1.5-1.3l-17.5-92.8c-0.2-0.8,0.3-1.6,1.1-1.8c0,0,0,0,0.1,0c0.5-0.1,1,0,1.4,0.3&#10;&#9;&#9;l22.6,20.1l13.4-22.6c0.4-0.7,1.4-1,2.1-0.5c0.3,0.1,0.5,0.4,0.6,0.6l11.9,23.2l19.7-20.4c0.6-0.6,1.6-0.6,2.2,0&#10;&#9;&#9;c0.4,0.4,0.5,0.9,0.4,1.4l-15,92.6c-0.3,0.8-1.1,1.2-1.9,1c-0.6-0.2-1.1-0.8-1.1-1.5l0,0l14.2-87.8l-17.8,18.5&#10;&#9;&#9;c-0.4,0.3-0.9,0.5-1.4,0.4c-0.5-0.1-0.9-0.4-1.2-0.9L351,155.3l-12.9,21.8c-0.2,0.4-0.6,0.7-1.1,0.8c-0.4,0.1-0.9-0.1-1.3-0.3&#10;&#9;&#9;L315,159.2l16.7,88.4c0.2,0.8-0.3,1.6-1.1,1.7c0,0-0.1,0-0.1,0L330.3,249.4L330.3,249.4z"/>\n</g>\n<g id="network_science-1-42">\n\t<path class="st0_science-1-42" d="M260.9,236.9c-23.5,0-39-5.6-43.1-16.4c-6.2-16.6,16.4-41.8,58.8-65.9c0.8-0.3,1.7-0.1,2.1,0.7&#10;&#9;&#9;c0.3,0.7,0.1,1.5-0.6,1.9c-40.4,22.8-62.9,47.2-57.3,62.1c5.5,14.7,38,18.5,82.9,9.7c20.8-4.2,41.2-10,61-17.5&#10;&#9;&#9;c18.4-6.8,36.3-14.9,53.5-24.4c42.4-23.4,66.2-48.4,60.5-63.7c-5.4-14.4-35.9-18.4-79.6-10.3c-0.8,0.3-1.7-0.2-1.9-1&#10;&#9;&#9;c-0.3-0.8,0.2-1.7,1-1.9c0.2-0.1,0.3-0.1,0.5-0.1c45.9-8.5,77-3.9,83,12.2c6.3,17.1-17.4,43-61.9,67.5c-17.4,9.5-35.4,17.7-54,24.5&#10;&#9;&#9;c-19.9,7.5-40.5,13.4-61.4,17.6C287.9,235.3,273.3,236.9,260.9,236.9z"/>\n\t<path class="st0_science-1-42" d="M438.3,236.9c-12.5,0-27.1-1.6-43.5-4.8c-20.8-4.2-41.3-10.1-61.2-17.6c-18.6-6.8-36.6-15-54-24.5&#10;&#9;&#9;c-44.5-24.5-68.2-50.4-61.8-67.5c6-16.2,37.1-20.7,83.1-12.2c0.9,0,1.5,0.7,1.5,1.6c0,0.9-0.7,1.5-1.6,1.5c-0.2,0-0.3,0-0.5-0.1&#10;&#9;&#9;l0,0c-43.1-8-74.4-4-79.7,10.3c-5.7,15.3,18,40.4,60.4,63.7c17.2,9.4,35.1,17.6,53.5,24.4c19.7,7.4,40,13.2,60.7,17.4&#10;&#9;&#9;c45,8.9,77.6,5.1,83-9.6s-17-39.2-57.3-62c-0.8-0.4-1.1-1.3-0.7-2c0,0,0-0.1,0-0.1c0.3-0.7,1.2-1.1,2-0.8c0.1,0,0.1,0.1,0.2,0.1&#10;&#9;&#9;c0.1,0,0.1,0.1,0.2,0.1c42.4,24,64.9,49.1,58.8,65.8C477.4,231.2,461.8,236.9,438.3,236.9z"/>\n\t<circle class="st3_science-1-42" cx="237.1" cy="231.6" r="11.5"/>\n\t<path class="st0_science-1-42" d="M237.1,244.6c-7.2,0-13-5.9-12.9-13.1s5.9-13,13.1-12.9c7.2,0,12.9,5.8,12.9,13c0,7.2-5.7,13-12.9,13&#10;&#9;&#9;C237.2,244.6,237.1,244.6,237.1,244.6z M237.1,221.6c-5.5,0-9.9,4.5-9.9,9.9s4.5,9.9,9.9,9.9c5.5,0,9.9-4.5,9.9-9.9l0,0l0,0&#10;&#9;&#9;C247,226.1,242.6,221.6,237.1,221.6L237.1,221.6z"/>\n\t<circle class="st4_science-1-42" cx="450.3" cy="171.4" r="11.5"/>\n\t<path class="st0_science-1-42" d="M450.3,184.5c-7.2,0-13.1-5.9-13.1-13.1c0-7.2,5.9-13.1,13.1-13.1c7.2,0,13.1,5.9,13.1,13.1l0,0&#10;&#9;&#9;C463.3,178.7,457.5,184.5,450.3,184.5z M450.3,161.5c-5.5,0-9.9,4.5-9.9,10s4.5,9.9,10,9.9c5.5,0,9.9-4.5,9.9-9.9l0,0&#10;&#9;&#9;C460.2,166,455.8,161.5,450.3,161.5z"/>\n\t<circle class="st5_science-1-42" cx="272" cy="104.3" r="11.5"/>\n\t<path class="st0_science-1-42" d="M272,117.3c-7.2,0-13.1-5.9-13.1-13.1c0-7.2,5.9-13.1,13.1-13.1c7.2,0,13.1,5.9,13.1,13.1l0,0&#10;&#9;&#9;C285,111.4,279.2,117.3,272,117.3z M272,94.2c-5.5,0-9.9,4.5-9.9,10c0,5.5,4.5,9.9,10,9.9c5.5,0,9.9-4.5,9.9-10c0,0,0,0,0,0&#10;&#9;&#9;C282,98.7,277.5,94.3,272,94.2z"/>\n</g>\n<g id="lines_science-1-42">\n\t<path class="st6_science-1-42" d="M248.5,279.4c-0.8,0-1.5-0.7-1.5-1.5c0,0,0,0,0,0V268c-0.1-0.8,0.4-1.6,1.3-1.7c0.8-0.1,1.6,0.4,1.7,1.3&#10;&#9;&#9;c0,0.2,0,0.3,0,0.5v9.9C250,278.7,249.3,279.3,248.5,279.4z"/>\n\t<path class="st6_science-1-42" d="M248.5,301c-0.8,0-1.5-0.7-1.5-1.5c0,0,0,0,0,0l0,0v-9.9c-0.1-0.8,0.4-1.6,1.3-1.7c0.8-0.1,1.6,0.4,1.7,1.3&#10;&#9;&#9;c0,0.2,0,0.3,0,0.5v9.9c0,0.8-0.6,1.5-1.4,1.5C248.6,301,248.5,301,248.5,301L248.5,301z"/>\n\t<path class="st6_science-1-42" d="M264.4,285.3h-9.9c-0.8,0.1-1.6-0.4-1.7-1.3c-0.1-0.8,0.4-1.6,1.3-1.7c0.2,0,0.3,0,0.5,0h9.9&#10;&#9;&#9;c0.8,0.1,1.4,0.9,1.3,1.7C265.5,284.6,265,285.2,264.4,285.3z"/>\n\t<path class="st6_science-1-42" d="M242.6,285.3h-9.9c-0.8,0.1-1.6-0.4-1.7-1.3c-0.1-0.8,0.4-1.6,1.3-1.7c0.2,0,0.3,0,0.5,0h9.9&#10;&#9;&#9;c0.8-0.1,1.6,0.4,1.7,1.3c0.1,0.8-0.4,1.6-1.3,1.7C242.9,285.3,242.8,285.3,242.6,285.3z"/>\n\t<path class="st6_science-1-42" d="M414.5,72.5c-0.8,0-1.5-0.6-1.5-1.5c0,0,0,0,0,0V61c-0.1-0.8,0.4-1.6,1.3-1.7c0.8-0.1,1.6,0.4,1.7,1.3&#10;&#9;&#9;c0,0.2,0,0.3,0,0.5v9.9C416,71.7,415.4,72.4,414.5,72.5C414.5,72.5,414.5,72.5,414.5,72.5L414.5,72.5z"/>\n\t<path class="st6_science-1-42" d="M414.5,94.1c-0.8,0-1.5-0.7-1.5-1.5c0,0,0,0,0,0v-9.9c-0.1-0.8,0.4-1.6,1.3-1.7c0.8-0.1,1.6,0.4,1.7,1.3&#10;&#9;&#9;c0,0.2,0,0.3,0,0.5v9.9C416,93.4,415.3,94.1,414.5,94.1C414.5,94.1,414.5,94.1,414.5,94.1L414.5,94.1z"/>\n\t<path class="st6_science-1-42" d="M430.3,78.4h-9.9c-0.8,0.1-1.6-0.4-1.7-1.3c-0.1-0.8,0.4-1.6,1.3-1.7c0.2,0,0.3,0,0.5,0h9.9&#10;&#9;&#9;c0.8,0,1.5,0.7,1.5,1.5c0,0.8-0.6,1.5-1.4,1.5C430.4,78.4,430.3,78.4,430.3,78.4L430.3,78.4z"/>\n\t<path class="st6_science-1-42" d="M408.6,78.4h-9.9c-0.8,0.1-1.6-0.4-1.7-1.3c-0.1-0.8,0.4-1.6,1.3-1.7c0.2,0,0.3,0,0.5,0h9.9&#10;&#9;&#9;c0.8,0.1,1.4,0.9,1.3,1.7C409.8,77.8,409.3,78.3,408.6,78.4z"/>\n\t<path class="st6_science-1-42" d="M441.1,266.1c-0.8,0-1.5-0.7-1.5-1.5v-8.2c0.1-0.8,0.9-1.4,1.7-1.3c0.6,0.1,1.1,0.6,1.3,1.3v8.2&#10;&#9;&#9;C442.6,265.4,441.9,266.1,441.1,266.1C441.1,266.1,441,266.1,441.1,266.1L441.1,266.1z"/>\n\t<path class="st6_science-1-42" d="M441.1,284.2c-0.8,0-1.5-0.7-1.5-1.5l0,0v-8.2c0.1-0.8,0.9-1.4,1.7-1.3c0.6,0.1,1.1,0.6,1.3,1.3v8.2&#10;&#9;&#9;C442.5,283.5,441.9,284.1,441.1,284.2L441.1,284.2z"/>\n\t<path class="st6_science-1-42" d="M454.1,271H446c-0.8-0.1-1.4-0.9-1.3-1.7c0.1-0.6,0.6-1.1,1.3-1.3h8.2c0.8-0.1,1.6,0.4,1.7,1.3&#10;&#9;&#9;c0.1,0.8-0.4,1.6-1.3,1.7C454.5,271,454.3,271,454.1,271L454.1,271z"/>\n\t<path class="st6_science-1-42" d="M436.2,271H428c-0.8-0.1-1.4-0.9-1.3-1.7c0.1-0.6,0.6-1.1,1.3-1.3h8.2c0.8-0.1,1.6,0.4,1.7,1.3&#10;&#9;&#9;c0.1,0.8-0.4,1.6-1.3,1.7C436.5,271,436.3,271,436.2,271L436.2,271z"/>\n</g>\n<g id="character_science-1-42">\n\t<g id="character-2_science-1-42">\n\t\t<path class="st7_science-1-42" d="M223.8,381.2c1.1-2.7,2-5.4,2.6-8.2c0.3-1.6,0.3-3.3-0.2-4.9c0-0.1,0-0.2,0-0.3l4.7,1.3l23.6,6.7l8.2,2.4&#10;&#9;&#9;&#9;c0,0,10.7-6,20.2-8.8s10.4,3.1,6.2,5.1c-7,3.3-9.2,5.2-9.2,5.2c6.1-0.9,19.9,2.4,20.8,5.8c0.3,1.4,5.6,14.5-7.2,17.2&#10;&#9;&#9;&#9;c-8.9,1.9-27.1-1.4-28.8-1.9l-43.2-12.3C222.3,386,223.1,383.6,223.8,381.2z"/>\n\t\t<path class="st0_science-1-42" d="M264.2,403.3l-43.4-12.4c-0.7-0.2-1.2-0.6-1.6-1.3c-0.3-0.6-0.4-1.3-0.2-2c0.7-2.1,1.5-4.6,2.2-7.1&#10;&#9;&#9;&#9;c0-0.1,0-0.2,0.1-0.2c1-2.5,1.9-5.1,2.4-7.8c0.3-1.2,0.2-2.5-0.2-3.7c-0.1-0.3-0.1-0.6-0.1-0.8v-0.3c0.1-1.4,1.3-2.6,2.7-2.5&#10;&#9;&#9;&#9;c0.2,0,0.4,0,0.6,0.1l35.5,10.1c6.3-3.4,12.9-6.3,19.8-8.5c8.8-2.6,11.1,1.4,11.6,2.7c1,2.7-0.5,5.8-3.5,7.2l-1.5,0.7&#10;&#9;&#9;&#9;c6.5,1.1,13.6,3.5,14.5,7.3l0.1,0.4c0.7,2.2,2.8,8.8-0.3,14.1c-1.7,3-4.8,5-9,5.8c-2.4,0.5-4.9,0.7-7.4,0.6&#10;&#9;&#9;&#9;C279,405.6,271.6,404.8,264.2,403.3z M298.2,386.3c-1.3-1.8-12.4-5-18-4.1c-1.4,0.2-2.7-0.8-2.9-2.2c-0.1-0.9,0.2-1.7,0.9-2.3&#10;&#9;&#9;&#9;c0.2-0.2,2.7-2.2,9.8-5.5c0.3-0.2,0.6-0.4,0.9-0.6c-0.3-0.2-1.8-0.8-5.3,0.3c-9.1,2.7-19.6,8.6-19.7,8.6c-0.6,0.3-1.3,0.4-2,0.2&#10;&#9;&#9;&#9;l-32.8-9.4c0,0.7-0.1,1.5-0.3,2.2c-0.6,2.9-1.5,5.8-2.7,8.5c-0.4,1.6-0.9,3.2-1.4,4.7l40.6,11.6c1.8,0.5,19.4,3.6,27.5,1.9&#10;&#9;&#9;&#9;c2.8-0.6,4.6-1.7,5.6-3.4c1.9-3.3,0.4-8.3-0.1-9.9C298.2,386.6,298.2,386.4,298.2,386.3L298.2,386.3z"/>\n\t\t<path class="st0_science-1-42" d="M274.3,393.1c0.3,0,0.5,0,0.8-0.1c3-0.7,5.5-2.7,6.9-5.4c1.2-2.8,1.3-6,0.3-8.8c-0.5-1.3-2-2-3.4-1.4&#10;&#9;&#9;&#9;c-1.3,0.5-1.9,1.9-1.5,3.2c0.5,1.6,0.5,3.2-0.1,4.8c-0.8,1.4-2.2,2.4-3.8,2.7c-1.4,0.4-2.1,1.9-1.7,3.2&#10;&#9;&#9;&#9;C272.2,392.3,273.2,393.1,274.3,393.1L274.3,393.1z"/>\n\t\t<path class="st2_science-1-42" d="M37.7,336.4c15-32.8,38.6-49,50-54s22.8-7.9,46.9-7.9c25.9,0,39.3,6.1,49.4,21.1c16,23.8,10.6,42.3,43.9,67.5&#10;&#9;&#9;&#9;c-2.9,7-5.1,14.2-7.4,21.5c-0.5,1.7-1.1,3.3-1.7,5c-10.8-6.5-29.7-19.2-43.4-35.4l-2.5,11.8v14.6H88V320&#10;&#9;&#9;&#9;c-9.7,7.8-17.5,17.7-22.8,29c-4.1,9.3-7.3,18.9-9.7,28.8l-29.3-7.5C29.1,358.7,32.9,347.4,37.7,336.4z"/>\n\t\t<rect x="124.8" y="283.5" class="st1_science-1-42 targetColor" width="20.3" height="132.4" style="fill: rgb(104, 225, 253);"/>\n\t\t<path class="st0_science-1-42" d="M147.2,418h-24.3V281.5h24.3V418z M126.8,414h16.3V285.5h-16.3V414z"/>\n\t\t<path class="st0_science-1-42" d="M217.5,391.8c-9.6-5.8-26.9-17.2-40.6-32.1l-1.4,6.6v14.3c0,1.4-1.2,2.6-2.6,2.6H88c-1.4,0-2.6-1.2-2.6-2.6&#10;&#9;&#9;&#9;v-54.9c-7.5,6.9-13.5,15.2-17.8,24.4c-4,9.2-7.2,18.7-9.5,28.4c-0.4,1.4-1.8,2.2-3.1,1.9l-29.3-7.5c-1.4-0.4-2.2-1.8-1.9-3.1&#10;&#9;&#9;&#9;c2.9-11.7,6.8-23.2,11.6-34.3l0,0c13.9-30.4,36.3-48.8,51.3-55.3c11.7-5.1,23.4-8.1,47.9-8.1c26.3,0,40.8,6.2,51.5,22.2&#10;&#9;&#9;&#9;c5.7,8.5,8.8,16.4,11.7,24c5.4,13.9,10.5,26.9,31.6,42.9c0.9,0.7,1.3,1.9,0.8,3c-2.4,5.9-4.4,12-6.4,18.3l-0.9,3&#10;&#9;&#9;&#9;c-0.4,1.2-0.8,2.4-1.2,3.6l-0.5,1.4c-0.3,0.7-0.8,1.3-1.6,1.6c-0.3,0.1-0.6,0.1-0.9,0.1C218.3,392.1,217.9,392,217.5,391.8z&#10;&#9;&#9;&#9; M193,320c-2.9-7.3-5.8-14.9-11.2-23c-9.8-14.5-22.6-19.9-47.2-19.9c-23.7,0-34.8,2.8-45.9,7.6c-3.1,1.5-31.2,14.6-48.7,52.8l0,0&#10;&#9;&#9;&#9;c-4.4,10-8,20.3-10.7,30.9l24.3,6.2c2.3-9.1,5.4-18.1,9.2-26.7c5.4-11.6,13.5-21.9,23.5-29.9c1.1-0.9,2.7-0.7,3.6,0.4&#10;&#9;&#9;&#9;c0.4,0.5,0.6,1,0.6,1.6v58h79.8v-12c0-0.2,0-0.4,0-0.5l2.5-11.9c0.3-1.4,1.7-2.3,3.1-2c0.6,0.1,1.1,0.4,1.4,0.8&#10;&#9;&#9;&#9;c12.5,14.8,29.5,26.6,40,33.2c0.2-0.6,0.4-1.3,0.6-1.9l0.9-2.9c1.8-5.6,3.6-11.3,5.8-16.9C203.8,347.7,198.3,333.6,193,320z"/>\n\t\t<polygon class="st0_science-1-42" points="77.4,439.6 88,380.6 172.9,380.6 179.8,439.6 &#9;&#9;"/>\n\t\t<path class="st0_science-1-42" d="M75.5,441.3c-0.5-0.6-0.7-1.4-0.6-2.1l10.6-59c0.2-1.2,1.3-2.2,2.5-2.2h84.9c1.3,0,2.4,1,2.6,2.3l6.8,59&#10;&#9;&#9;&#9;c0.2,1.4-0.9,2.7-2.3,2.9c-0.1,0-0.2,0-0.3,0H77.4C76.7,442.2,76,441.9,75.5,441.3z M170.6,383.2H90.2l-9.6,53.9h96.3L170.6,383.2&#10;&#9;&#9;&#9;z"/>\n\t\t<polyline class="st2_science-1-42" points="124.8,372.1 124.8,440.5 74.2,440.5 88,378 &#9;&#9;"/>\n\t\t<path class="st0_science-1-42" d="M126.8,442.5H71.8L86,377.6c0.2-1.1,1.2-1.8,2.3-1.7c1.1,0.2,1.8,1.2,1.7,2.3c0,0.1,0,0.1,0,0.2l-13.2,60&#10;&#9;&#9;&#9;h46.1v-66.4c0-1.1,0.9-2,2-2s2,0.9,2,2L126.8,442.5z"/>\n\t\t<path class="st7_science-1-42" d="M49.4,363.3c-6.3,3.6-12.6,7.4-18.8,11.1C40.8,393.2,54,418,58.3,424.8C64.1,434,70,442,73.6,443&#10;&#9;&#9;&#9;s12.8-5.7,14.4-8s-8.6-11.9-8.6-11.9l6.4-3.6c-0.3-2.4-11.2-8.2-11.2-8.2C74.2,410.3,60,383,49.4,363.3z"/>\n\t\t<path class="st0_science-1-42" d="M73,445.5c-2.7-0.7-6.8-3.5-16.8-19.3c-3.2-5.1-11-19.5-19.3-34.8c-2.9-5.4-5.8-10.8-8.5-15.7&#10;&#9;&#9;&#9;c-0.7-1.2-0.2-2.7,0.9-3.4c6-3.7,12.4-7.5,18.9-11.2c1.2-0.7,2.8-0.3,3.5,0.9c0,0,0,0,0,0.1c9.4,17.4,22.3,42.2,24.8,47.3&#10;&#9;&#9;&#9;c11.4,6.1,11.7,8.8,11.8,9.7c0.1,1-0.4,2.1-1.3,2.6l-3.3,1.9c9.1,9.1,7.2,11.8,6.4,12.9c-1.8,2.5-10.4,9.1-15.9,9.1&#10;&#9;&#9;&#9;C73.9,445.6,73.4,445.6,73,445.5z M77.7,425c-0.6-0.6-0.9-1.4-0.8-2.2c0.1-0.8,0.6-1.5,1.3-2l3.6-2c-2.7-1.9-5.5-3.7-8.4-5.2&#10;&#9;&#9;&#9;c-0.5-0.3-0.9-0.7-1.2-1.3c-0.6-1.3-13.2-25.6-23.8-45.4c-4.8,2.8-9.7,5.7-14.3,8.5c2.4,4.4,4.8,9,7.3,13.6&#10;&#9;&#9;&#9;c7.8,14.5,15.9,29.5,19.1,34.5c9.2,14.5,12.7,16.7,13.8,17c1.9,0.4,9-4.2,11.3-6.5C84.8,432.3,81.3,428.3,77.7,425z M74.6,411.3&#10;&#9;&#9;&#9;L74.6,411.3z"/>\n\t\t<path class="st8_science-1-42" d="M100.6,116c0,0-43.2-2.3-49.7,38.7c-4.3,27.4-6,54.5-15,81.1c26.3,22.8,63.4,32.2,97.7,26.3&#10;&#9;&#9;&#9;s65.6-26.6,85.9-54.9c-9.6-20.9-16.6-42.9-20.9-65.5c-3-15.9-8.2-25.5-22.9-33.9c-12.6-7.1-27.1-10.3-41.5-9.2&#10;&#9;&#9;&#9;c-6.8,0.5-13.5,2.3-19.6,5.3C112.1,105.1,101.5,116.1,100.6,116z"/>\n\t\t<path class="st0_science-1-42" d="M34.2,237.8c-0.8-0.7-1.1-1.8-0.8-2.8c6.6-19.5,9.2-38.9,11.9-59.5c0.9-6.9,1.9-14.1,3-21.2&#10;&#9;&#9;&#9;c6.2-39.1,44.4-40.9,51.3-40.9h0.2c1-0.8,3.4-3,5.1-4.7c4.2-4,6.9-6.5,8.4-7.2c6.4-3.2,13.4-5.1,20.6-5.5c15-1.1,29.9,2.2,43,9.6&#10;&#9;&#9;&#9;c16.4,9.3,21.2,20.1,24.2,35.7c4.3,22.4,11.2,44.2,20.7,64.9c0.4,0.8,0.3,1.8-0.2,2.6c-21.2,29.6-53.1,50-87.5,56&#10;&#9;&#9;&#9;c-7,1.2-14,1.8-21.1,1.8C84,266.4,55.6,256.3,34.2,237.8z M196,142.2c-2.7-14.4-6.9-23.8-21.6-32.2c-12.2-6.8-26.1-9.9-40-8.9&#10;&#9;&#9;&#9;c-6.5,0.4-12.8,2.1-18.6,5c-1,0.5-4.9,4.2-7.2,6.4c-5.9,5.6-6.6,6.1-8.1,6.1l0,0c-7.3-0.1-14.6,1.2-21.5,3.9&#10;&#9;&#9;&#9;c-14.4,5.7-23,16.7-25.5,32.6c-1.1,7-2.1,14.2-3,21.1c-2.6,19.4-5.3,39.4-11.6,58.8c25.3,21.2,60.4,30.4,94.2,24.6&#10;&#9;&#9;&#9;c32.6-5.6,62.9-24.8,83.3-52.7C207.1,186.2,200.3,164.5,196,142.2z M100.5,116L100.5,116z M100.7,113.4L100.7,113.4z"/>\n\t\t<path class="st2_science-1-42" d="M228.4,357.9l11.2,6.6c1,0.6,1.3,1.8,0.7,2.8l-16.2,27.4c-0.6,1-1.8,1.3-2.8,0.7l-11.2-6.6&#10;&#9;&#9;&#9;c-1-0.6-1.3-1.8-0.7-2.8l16.2-27.4C226.2,357.6,227.4,357.3,228.4,357.9z"/>\n\t\t<path class="st0_science-1-42" d="M217.3,396l-5.7-3.4c-3.7-2.2-4.9-7-2.7-10.7l12.9-21.9c2.2-3.7,7-4.9,10.7-2.7l5.7,3.4&#10;&#9;&#9;&#9;c3.7,2.2,4.9,7,2.7,10.7L228,393.2c-1,1.8-2.8,3.1-4.8,3.6c-0.6,0.2-1.3,0.2-1.9,0.2C219.9,397.1,218.5,396.7,217.3,396z&#10;&#9;&#9;&#9; M227.8,361.5c-0.7,0.2-1.3,0.6-1.6,1.2l-12.9,21.9c-0.7,1.3-0.3,2.9,0.9,3.6l0,0l5.7,3.4c1.3,0.7,2.9,0.3,3.6-0.9l12.9-21.9&#10;&#9;&#9;&#9;c0.7-1.3,0.3-2.9-0.9-3.6l-5.7-3.4c-0.4-0.2-0.9-0.4-1.3-0.4C228.3,361.4,228,361.4,227.8,361.5L227.8,361.5z"/>\n\t\t<path class="st7_science-1-42" d="M124.8,265.8h20.3l0,0v17c0,1.9-1.5,3.4-3.3,3.4h0h-13.6c-1.9,0-3.3-1.5-3.3-3.4l0,0L124.8,265.8L124.8,265.8&#10;&#9;&#9;&#9;L124.8,265.8z"/>\n\t\t<path class="st0_science-1-42" d="M122.2,277.5v-11.7c0-1.4,1.2-2.6,2.6-2.6h20.3c1.4,0,2.6,1.2,2.6,2.6v11.7c0,6.2-5,11.2-11.2,11.2h-3.1&#10;&#9;&#9;&#9;C127.3,288.7,122.3,283.7,122.2,277.5z M127.4,268.3v9.1c0,3.3,2.7,6,6.1,6h3.1c3.3,0,6-2.7,6.1-6v-9.1H127.4z"/>\n\t\t<ellipse class="st7_science-1-42" cx="187.7" cy="215" rx="15.2" ry="17"/>\n\t\t<path class="st0_science-1-42" d="M169.9,215c0-10.8,8-19.6,17.8-19.6s17.8,8.8,17.8,19.6s-8,19.6-17.8,19.6S169.9,225.9,169.9,215z M175,215&#10;&#9;&#9;&#9;c0,8,5.7,14.4,12.7,14.4s12.7-6.4,12.7-14.4s-5.7-14.4-12.7-14.4S175,207.1,175,215L175,215z"/>\n\t\t<path class="st7_science-1-42" d="M134.4,270.5c-33.4,0-63.4-41.3-63.4-74.2l8,3c0,0,41.6-34.3,36.1-53.8c0,0,12.3,14.6,30,14.6&#10;&#9;&#9;&#9;c32.5-0.1,45.2-8.7,45.2-8.7v59.5C190.2,243.9,167.8,270.5,134.4,270.5z"/>\n\t\t<path class="st0_science-1-42" d="M68.4,196.4c0-1.4,1.2-2.6,2.6-2.6c0.3,0,0.6,0.1,0.9,0.2l6.6,2.5c11.9-10,38.2-36,34.1-50.2&#10;&#9;&#9;&#9;c-0.4-1.4,0.4-2.8,1.8-3.2c1-0.3,2,0,2.7,0.8c0.1,0.1,11.8,13.6,27.9,13.6h0.1c31.1-0.1,43.6-8.2,43.8-8.2&#10;&#9;&#9;&#9;c1.2-0.8,2.8-0.5,3.6,0.7c0.3,0.4,0.4,0.9,0.4,1.4v59.5c0,36-24.6,62.2-58.4,62.2C99.5,273.1,68.4,230.2,68.4,196.4z M145,162.7&#10;&#9;&#9;&#9;L145,162.7c-12.1,0-21.6-6.2-27.1-10.7c-1,8-6.7,17.9-17,29.5c-6.3,7.1-13.1,13.8-20.4,19.9c-0.7,0.6-1.7,0.8-2.6,0.4l-4.3-1.6&#10;&#9;&#9;&#9;c2.2,36.3,34.8,67.8,60.7,67.8c30.9,0,53.2-24,53.2-57v-55.3C181.5,158.3,168.1,162.6,145,162.7z"/>\n\t\t<ellipse class="st0_science-1-42" cx="127" cy="200.6" rx="5.5" ry="5.5"/>\n\t\t<circle class="st0_science-1-42" cx="168.9" cy="199.9" r="5.5"/>\n\t\t<path class="st0_science-1-42" d="M140.4,220.5c-1.4-0.2-2.3-1.6-2.1-3s1.6-2.3,3-2.1c2.4,0.4,4.8,0.5,7.2,0.2c-0.2-2.1-2.1-7.2-4.6-11.9&#10;&#9;&#9;&#9;c-0.7-1.3-0.2-2.8,1.1-3.5s2.8-0.2,3.5,1.1c2.5,4.7,6.4,13.2,4.7,17c-0.5,1.1-1.4,1.9-2.6,2.2c-1.5,0.3-3.1,0.5-4.7,0.5&#10;&#9;&#9;&#9;C144.1,221,142.2,220.8,140.4,220.5z M148.4,216.3L148.4,216.3z"/>\n\t\t<path class="st7_science-1-42" d="M83,200.6c0,0-14.6-10.1-22.4,2.9s-0.3,35.1,23.8,28.6"/>\n\t\t<path class="st0_science-1-42" d="M76.3,235.8c2.9,0,5.8-0.4,8.7-1.2c1.4-0.4,2.2-1.8,1.8-3.2c-0.4-1.4-1.8-2.2-3.2-1.8&#10;&#9;&#9;&#9;c-8.9,2.4-16.1,0.7-20.2-4.8s-4.4-13.9-0.7-20c1.7-2.9,3.9-4.6,6.6-5.2c5.8-1.2,12.1,3,12.1,3.1c1.2,0.8,2.8,0.5,3.6-0.7&#10;&#9;&#9;&#9;c0.8-1.2,0.5-2.8-0.7-3.6c-0.3-0.2-8.1-5.6-16.1-3.9c-4.1,0.9-7.5,3.4-10,7.5c-4.8,8-4.4,18.6,1,25.8&#10;&#9;&#9;&#9;C63.2,233.1,69.2,235.8,76.3,235.8z"/>\n\t\t<path class="st2_science-1-42" d="M65.1,363.9l1.1,12.6c0.1,1.2-0.8,2.3-2,2.4l-37.7,3.4c-1.2,0.1-2.3-0.8-2.4-2l-1.1-12.6&#10;&#9;&#9;&#9;c-0.1-1.2,0.8-2.3,2-2.4l37.7-3.4C63.9,361.8,65,362.7,65.1,363.9z"/>\n\t\t<path class="st0_science-1-42" d="M21.2,377l-0.5-5.7c-0.4-4.5,2.9-8.5,7.5-8.9c0,0,0,0,0,0l30.8-2.7c4.5-0.4,8.6,2.9,9,7.5c0,0,0,0,0,0&#10;&#9;&#9;&#9;l0.5,5.7c0.4,4.5-2.9,8.5-7.5,8.9c0,0,0,0,0,0l-30.8,2.7c-0.2,0-0.5,0-0.7,0C25.2,384.5,21.6,381.3,21.2,377z M59.5,364.8&#10;&#9;&#9;&#9;l-30.8,2.7c-1.7,0.1-3,1.6-2.8,3.3c0,0,0,0,0,0l0,0l0.5,5.7c0.1,0.8,0.5,1.6,1.1,2.1c0.6,0.5,1.4,0.8,2.3,0.7l30.8-2.7&#10;&#9;&#9;&#9;c1.7-0.1,2.9-1.6,2.8-3.3c0,0,0,0,0,0l-0.5-5.7c-0.1-0.8-0.5-1.6-1.1-2.1c-0.6-0.5-1.3-0.7-2-0.7L59.5,364.8z"/>\n\t\t<path class="st2_science-1-42" d="M153.8,229l-23.2,1.1c0,0,2,23.8,10.3,26.1C149.2,258.5,154.8,243.1,153.8,229z"/>\n\t\t<path class="st0_science-1-42" d="M140.2,258.7c-9.6-2.6-11.9-24.1-12.2-28.3c-0.1-0.7,0.2-1.4,0.6-1.9c0.5-0.5,1.1-0.8,1.8-0.9l23.2-1.1&#10;&#9;&#9;&#9;c1.4-0.1,2.6,1,2.7,2.4c0.9,11.6-2.5,23.4-8,28C146.1,258.8,143.1,259.5,140.2,258.7L140.2,258.7z M133.4,232.6&#10;&#9;&#9;&#9;c1.1,8.7,4.1,20,8.2,21.1c1.2,0.3,2.6,0,3.5-0.9c3.8-3.2,6.4-12.1,6.3-21.1L133.4,232.6z"/>\n\t\t<path class="st0_science-1-42" d="M175.4,356.7c1,0,2-0.6,2.4-1.6c9.9-23-3.4-49.3-4-50.4c-0.7-1.3-2.2-1.8-3.5-1.1c-1.3,0.7-1.8,2.2-1.1,3.5&#10;&#9;&#9;&#9;c0.1,0.2,12.7,25.3,3.8,46c-0.6,1.3,0,2.8,1.3,3.4c0,0,0,0,0,0C174.7,356.7,175,356.7,175.4,356.7z"/>\n\t</g>\n\t<polyline class="st2_science-1-42" points="145.2,376.6 145.2,440.5 179.8,440.5 172.9,378 &#9;"/>\n\t<path class="st0_science-1-42" d="M182,442.5h-38.8v-65.9c0-1.1,0.9-2,2-2s2,0.9,2,2v61.9h30.4l-6.6-60.2c-0.1-1.1,0.7-2.1,1.8-2.2&#10;&#9;&#9;s2.1,0.7,2.2,1.8L182,442.5z"/>\n\t<path class="st0_science-1-42" d="M122.2,222.4c-12.4,0-22.4-10.1-22.4-22.5c0-12.4,10.1-22.4,22.5-22.4c12.4,0,22.4,10.1,22.4,22.5c0,0,0,0,0,0&#10;&#9;&#9;C144.7,212.4,134.6,222.4,122.2,222.4z M122.2,181.5c-10.2,0-18.4,8.3-18.4,18.5c0,10.2,8.3,18.4,18.5,18.4&#10;&#9;&#9;c10.2,0,18.4-8.2,18.4-18.4C140.7,189.8,132.5,181.5,122.2,181.5C122.3,181.5,122.3,181.5,122.2,181.5z"/>\n\t<path class="st0_science-1-42" d="M169.9,222.4c-12.4,0-22.4-10.1-22.4-22.5c0-12.4,10.1-22.4,22.5-22.4c12.4,0,22.4,10.1,22.4,22.5c0,0,0,0,0,0&#10;&#9;&#9;C192.3,212.4,182.2,222.4,169.9,222.4z M169.9,181.5c-10.2,0-18.4,8.3-18.4,18.5c0,10.2,8.3,18.4,18.5,18.4&#10;&#9;&#9;c10.2,0,18.4-8.2,18.4-18.4C188.3,189.8,180.1,181.5,169.9,181.5C169.9,181.5,169.9,181.5,169.9,181.5z"/>\n</g>\n</svg>
\.


--
-- Data for Name: curriculum_matierecontexte; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_matierecontexte (id, est_actif, date_creation, date_modification, titre, ordre, description, couleur, svg_icon, matiere_id, niveau_id) FROM stdin;
9	t	2025-08-15 07:25:10.902014+00	2025-08-15 07:25:10.902045+00	Mathématiques (France, CE1)	0	\N	#3b82f6	\N	1	10
10	t	2025-08-15 07:25:15.864844+00	2025-08-15 07:25:15.864874+00	Mathématiques (France, CE2)	0	\N	#3b82f6	\N	1	11
11	t	2025-08-15 07:25:19.469882+00	2025-08-15 07:25:19.469909+00	Mathématiques (France, CM1)	0	\N	#3b82f6	\N	1	12
12	t	2025-08-15 07:25:23.98181+00	2025-08-15 07:25:23.981836+00	Mathématiques (France, 6ème)	0	\N	#3b82f6	\N	1	14
13	t	2025-08-15 07:25:29.919201+00	2025-08-15 07:25:29.919211+00	Mathématiques (France, 4ème)	0	\N	#3b82f6	\N	1	16
14	t	2025-08-15 07:25:37.318641+00	2025-08-15 07:25:37.318663+00	Mathématiques (France, CM2)	0	\N	#3b82f6	\N	1	13
20	t	2025-08-15 07:42:48.467144+00	2025-08-15 07:42:48.467172+00	Physique (France, 5ème)	0	\N	#3b82f6	\N	7	15
21	t	2025-08-15 07:42:52.877176+00	2025-08-15 07:42:52.877199+00	Physique (France, 4ème)	0	\N	#3b82f6	\N	7	16
22	t	2025-08-15 13:26:58.00334+00	2025-08-15 13:26:58.003381+00	Mathématiques (France, 3ème)	0	\N	#3b82f6	\N	1	17
23	t	2025-08-15 13:27:03.022435+00	2025-08-15 13:27:03.022448+00	Mathématiques (France, 2nde)	0	\N	#3b82f6	\N	1	18
24	t	2025-08-15 13:27:06.710366+00	2025-08-15 13:27:06.710382+00	Mathématiques (France, 1ère)	0	\N	#3b82f6	\N	1	19
25	t	2025-08-15 13:27:23.310802+00	2025-08-15 13:27:23.310819+00	Mathématiques (France, Terminale)	0	\N	#3b82f6	\N	1	20
26	t	2025-08-16 09:04:32.161992+00	2025-08-16 09:04:32.162017+00	Physique (France, Terminale)	0	\N	#3b82f6	\N	7	20
30	t	2025-09-12 14:03:58.977171+00	2025-09-12 14:03:58.977186+00	Physique (France, 3ème)	0	\N	#3b82f6	\N	7	17
31	t	2025-09-12 14:04:02.721647+00	2025-09-12 14:04:02.721672+00	Physique (France, 2nde)	0	\N	#3b82f6	\N	7	18
32	t	2025-09-12 14:04:08.851626+00	2025-09-12 14:04:08.851653+00	Physique (France, 1ère)	0	\N	#3b82f6	\N	7	19
38	t	2025-09-12 18:51:51.068768+00	2025-09-12 18:51:51.068839+00	Mathématiques (France, 5ème)	0	\N	#3b82f6	\N	1	15
39	t	2025-09-12 19:10:10.083368+00	2025-09-12 19:10:10.083425+00	Informatique (France, CE1)	0	\N	#3b82f6	\N	22	10
\.


--
-- Data for Name: curriculum_notion; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_notion (id, est_actif, date_creation, date_modification, titre, ordre, description, couleur, svg_icon, theme_id) FROM stdin;
3	t	2025-09-12 12:36:29.504049+00	2025-09-12 12:45:33.251398+00	Décomposition en unités, dizaines et centaines	0	\N	#3b82f6	\N	12
4	t	2025-09-12 12:47:37.384327+00	2025-09-12 12:47:37.384352+00	Dénombrement et représentations	0	\N	#3b82f6	\N	12
5	t	2025-09-12 12:48:09.938534+00	2025-09-12 12:48:09.938566+00	Comparaison et ordonnancement des nombres	0	\N	#3b82f6	\N	12
6	t	2025-09-12 12:48:14.520023+00	2025-09-12 12:48:14.520074+00	Repérage dans la suite des nombres	0	\N	#3b82f6	\N	12
2	t	2025-09-11 18:44:15.293973+00	2025-09-12 12:48:46.209404+00	Lecture et écriture des nombres entiers	0	\N	#3b82f6	\N	12
7	t	2025-09-12 12:54:57.189888+00	2025-09-12 12:58:50.812827+00	Figures planes	0	\N	#3b82f6	\N	3
9	t	2025-09-12 12:55:43.386721+00	2025-09-12 12:59:43.26453+00	Repérage et positions dans l’espace	0	\N	#3b82f6	\N	3
8	t	2025-09-12 12:55:10.973232+00	2025-09-12 12:59:52.281859+00	Solides usuels	0	\N	#3b82f6	\N	3
10	t	2025-09-12 13:01:11.095445+00	2025-09-12 13:01:11.095487+00	Repérage sur plan ou quadrillage	0	\N	#3b82f6	\N	3
11	t	2025-09-12 13:03:24.246302+00	2025-09-12 13:03:24.246331+00	Tracé et instruments géométriques	0	\N	#3b82f6	\N	3
12	t	2025-09-12 13:29:00.483102+00	2025-09-12 13:29:00.483125+00	Longueurs	0	\N	#3b82f6	\N	2
13	t	2025-09-12 13:29:14.030096+00	2025-09-12 13:29:14.030108+00	Masses	0	\N	#3b82f6	\N	2
14	t	2025-09-12 13:29:27.886861+00	2025-09-12 13:29:27.886886+00	Contenances	0	\N	#3b82f6	\N	2
15	t	2025-09-12 13:29:47.295564+00	2025-09-12 13:29:47.295578+00	Lecture de l’heure et durées	0	\N	#3b82f6	\N	2
16	t	2025-09-12 13:29:57.510029+00	2025-09-12 13:29:57.510042+00	Monnaie	0	\N	#3b82f6	\N	2
17	t	2025-09-12 13:34:51.154888+00	2025-09-12 13:34:51.154901+00	Automatisation des faits numériques	0	\N	#3b82f6	\N	1
18	t	2025-09-12 13:35:05.337917+00	2025-09-12 13:35:05.337945+00	Calcul posé	0	\N	#3b82f6	\N	1
28	t	2025-09-12 14:21:24.956264+00	2025-09-12 14:21:59.94313+00	Vecteurs, droites et plans dans l’espace	0	\N	#3b82f6	\N	15
29	t	2025-09-12 14:22:16.644236+00	2025-09-12 14:22:16.644262+00	Produit scalaire et orthogonalité	0	\N	#3b82f6	\N	15
31	t	2025-09-12 14:23:19.278505+00	2025-09-12 14:23:19.278519+00	Représentations paramétriques et équations cartésiennes	0	\N	#3b82f6	\N	15
33	t	2025-09-12 14:31:18.972928+00	2025-09-12 14:31:18.972943+00	Combinaisons linéaires, indépendance	0	\N	#3b82f6	\N	15
34	t	2025-09-12 14:39:41.121431+00	2025-09-12 14:39:41.121445+00	Loi binomiale	0	\N	#3b82f6	\N	17
36	t	2025-09-12 14:40:47.77157+00	2025-09-12 14:40:47.771584+00	La loi des grands nombres	0	\N	#3b82f6	\N	17
37	t	2025-09-12 14:42:00.489435+00	2025-09-12 14:42:00.489453+00	Dénombrement	0	\N	#3b82f6	\N	17
35	t	2025-09-12 14:40:08.7487+00	2025-09-12 14:42:30.687287+00	Expériences aléatoires	0	\N	#3b82f6	\N	17
38	t	2025-09-12 14:53:28.074874+00	2025-09-12 14:53:28.074889+00	Listes	0	\N	#3b82f6	\N	18
39	t	2025-09-12 14:53:40.573134+00	2025-09-12 14:53:40.573148+00	Conditions et logique	0	\N	#3b82f6	\N	18
40	t	2025-09-12 14:53:56.12761+00	2025-09-12 14:53:56.127625+00	Boucles / Itérations	0	\N	#3b82f6	\N	18
19	t	2025-08-16 09:18:42.150418+00	2025-09-14 17:09:07.342754+00	Suites Numériques	1	\N	#3b82f6	\N	16
20	t	2025-08-16 09:20:10.42091+00	2025-09-14 17:09:28.330017+00	Limites des fonctions	2	\N	#3b82f6	\N	16
21	t	2025-08-16 09:22:17.936208+00	2025-09-14 17:09:38.484046+00	Dérivation	3	\N	#3b82f6	\N	16
22	t	2025-08-16 09:23:11.619814+00	2025-09-14 17:09:50.035712+00	Continuité des fonctions	4	\N	#3b82f6	\N	16
23	t	2025-08-16 09:23:31.55498+00	2025-09-14 17:10:02.434154+00	Fonction logarithme	5	\N	#3b82f6	\N	16
24	t	2025-08-16 09:24:39.70426+00	2025-09-14 17:10:10.582781+00	Fonctions trigonométriques	6	\N	#3b82f6	\N	16
25	t	2025-08-16 09:25:43.567478+00	2025-09-14 17:10:23.121128+00	Primitives	7	\N	#3b82f6	\N	16
26	t	2025-08-16 09:28:37.024047+00	2025-09-14 17:10:39.620106+00	Équations différentielles	8	\N	#3b82f6	\N	16
32	t	2025-09-12 14:29:15.568021+00	2025-09-14 17:11:07.901921+00	Fonction exponentielle	10	\N	#3b82f6	\N	16
27	t	2025-08-16 09:28:51.99492+00	2025-09-14 17:18:39.362376+00	Calcul Intégral	9	\N	#3b82f6	\N	16
47	t	2025-09-17 12:59:21.689267+00	2025-09-17 12:59:21.68928+00	physique test	0	\N	#3b82f6	\N	13
\.


--
-- Data for Name: curriculum_theme; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.curriculum_theme (id, est_actif, date_creation, date_modification, titre, ordre, description, couleur, svg_icon, matiere_id, contexte_id) FROM stdin;
16	t	2025-08-16 09:06:41.129077+00	2025-08-16 09:06:41.129103+00	Analyse	2		#3b82f6	\N	1	25
17	t	2025-08-16 09:06:52.399357+00	2025-08-16 09:06:52.399376+00	Dénombrement et probabilités	3		#3b82f6	\N	1	25
18	t	2025-08-16 09:07:06.077882+00	2025-08-16 09:07:06.077898+00	Algorithmique et programmation	4		#3b82f6	\N	1	25
1	t	2025-09-11 18:15:56.384658+00	2025-09-11 18:15:56.384678+00	Calculs	2		#e13bf7	\N	1	9
2	t	2025-09-11 18:16:27.948002+00	2025-09-11 18:16:27.948018+00	Grandeurs et Mesures	3		#f73b96	\N	1	9
3	t	2025-09-11 18:16:50.71503+00	2025-09-11 18:16:50.715043+00	Espace et Géométrie	4		#3b82f6	\N	1	9
12	t	2025-08-15 12:00:43.849763+00	2025-09-12 12:34:32.143631+00	Nombres Entiers Jusqu’à 999	1		#3b82f6		1	9
4	t	2025-09-12 13:56:01.081358+00	2025-09-12 13:56:01.081381+00	Nombres Entiers Jusqu’à 9999	1		#3b82f6	\N	1	10
5	t	2025-09-12 13:58:22.361175+00	2025-09-12 13:58:45.992498+00	Calcul	2		#f73bde	\N	1	10
15	t	2025-08-16 09:06:18.033122+00	2025-09-12 14:32:00.538235+00	Algèbre et Géométrie	1		#3b82f6	\N	1	25
7	t	2025-09-12 14:58:45.87216+00	2025-09-12 14:58:45.872179+00	Géométrie	3		#3b82f6	\N	1	24
9	t	2025-09-12 15:06:29.145166+00	2025-09-12 15:06:33.781015+00	Organisation et transformation de la matière	1		#3b82f6	\N	7	20
10	t	2025-09-12 15:06:49.906866+00	2025-09-12 15:06:49.906883+00	Mouvement et interactions	2		#3b82f6	\N	7	20
11	t	2025-09-12 15:06:59.384706+00	2025-09-12 15:06:59.384724+00	L’énergie et ses conversions	3		#3b82f6	\N	7	20
35	t	2025-09-14 21:16:21.155622+00	2025-09-14 21:16:21.155637+00	Algèbre	0	\N	#3b82f6	\N	1	24
36	t	2025-09-14 21:16:21.181092+00	2025-09-14 21:16:21.181104+00	Algèbre	0	\N	#3b82f6	\N	1	23
13	t	2025-09-12 15:07:40.90322+00	2025-09-17 13:02:39.67304+00	L'utilisation des signaux pour observer et communiquer	4		#3b82f6	\N	7	26
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-08-09 15:06:10.825499+00	3	admin@admin.com	3		6	2
2	2025-08-09 15:06:10.825566+00	1	admin@test.com	3		6	2
3	2025-08-09 15:06:47.52598+00	1	France	1	[{"added": {}}]	20	2
4	2025-08-09 15:07:04.71658+00	1	France - 6ème	1	[{"added": {}}]	21	2
5	2025-08-09 17:58:51.72064+00	2	France - 5ème	1	[{"added": {}}]	21	2
6	2025-08-09 17:58:57.505925+00	2	France - 5ème	2	[{"changed": {"fields": ["Ordre"]}}]	21	2
7	2025-08-09 17:58:57.534989+00	1	France - 6ème	2	[{"changed": {"fields": ["Ordre"]}}]	21	2
8	2025-08-09 21:42:50.367426+00	4	admin@optitab.com	3		6	2
9	2025-08-10 10:57:51.787167+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Civilit\\u00e9", "Date de naissance", "Num\\u00e9ro de t\\u00e9l\\u00e9phone", "Pays", "Niveau scolaire"]}}]	6	2
10	2025-08-10 12:32:57.362414+00	6	France - 5ème - Phyisque	1	[{"added": {}}]	22	2
11	2025-08-10 12:33:03.850199+00	1	France - 6ème - Mathématiques	2	[]	22	2
12	2025-08-10 12:34:32.043178+00	8	France - 5ème - Chimie	1	[{"added": {}}]	22	2
13	2025-08-10 12:34:44.357483+00	6	France - 5ème - RDM	2	[{"changed": {"fields": ["Titre", "Ordre"]}}]	22	2
14	2025-08-10 12:39:20.349429+00	7	France - 5ème - Physique	2	[{"changed": {"fields": ["Ordre"]}}]	22	2
15	2025-08-10 12:39:20.370846+00	6	France - 5ème - RDM	2	[{"changed": {"fields": ["Ordre"]}}]	22	2
16	2025-08-10 12:39:20.391341+00	9	France - 6ème - Chimie	2	[{"changed": {"fields": ["Ordre"]}}]	22	2
17	2025-08-10 14:14:24.118896+00	1	Mathématiques - Géométrie	2	[]	23	2
18	2025-08-10 14:14:32.529038+00	1	Mathématiques - Géométrie	2	[]	23	2
19	2025-08-10 14:15:44.252962+00	3	Mathématiques - TEST2	1	[{"added": {}}]	23	2
20	2025-08-10 14:16:02.130501+00	1	Chimie - Géométrie	2	[{"changed": {"fields": ["Matiere"]}}]	23	2
21	2025-08-10 14:16:20.665571+00	1	Géométrie - Les Longueurs	2	[]	24	2
22	2025-08-10 15:32:07.182079+00	3	CA Canada	1	[{"added": {}}]	20	2
23	2025-08-10 15:35:33.003946+00	3	Lebanon - Terminal	1	[{"added": {}}]	21	2
24	2025-08-10 15:35:51.705338+00	4	Canada - Grade8	1	[{"added": {}}]	21	2
25	2025-08-10 15:56:48.339198+00	5	admin@test.com	3		6	2
26	2025-08-10 16:09:28.638163+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau scolaire"]}}]	6	2
27	2025-08-10 16:09:34.993243+00	2	anthonytabet.c@gmail.com	2	[]	6	2
28	2025-08-11 09:27:39.026638+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Civilite", "Date de naissance", "Num\\u00e9ro de t\\u00e9l\\u00e9phone"]}}]	6	2
29	2025-08-11 12:38:12.009542+00	2	Lebanon - 5ème	2	[{"changed": {"fields": ["Ordre"]}}]	21	2
30	2025-08-11 12:38:12.037742+00	3	Lebanon - Terminal	2	[{"changed": {"fields": ["Ordre"]}}]	21	2
31	2025-08-11 12:38:12.066944+00	4	Canada - Grade8	2	[{"changed": {"fields": ["Ordre"]}}]	21	2
32	2025-08-11 13:12:45.358265+00	10	France - 6ème - azaz	3		22	2
33	2025-08-11 23:05:13.19305+00	12	English	2	[{"changed": {"fields": ["Ordre"]}}]	22	2
34	2025-08-11 23:05:13.268092+00	1	Mathématiques	2	[{"changed": {"fields": ["Ordre"]}}]	22	2
35	2025-08-11 23:05:43.90735+00	6	test@example.com	3		6	2
36	2025-08-13 08:44:58.984216+00	5	Arabe - testtt	2	[{"changed": {"fields": ["Contexte"]}}]	23	2
37	2025-08-13 16:20:42.241804+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
38	2025-08-13 23:36:34.128128+00	7	a@gmail.cpm	1	[{"added": {}}]	6	2
39	2025-08-13 23:36:48.103534+00	7	a@gmail.cpm	2	[]	6	2
40	2025-08-13 23:37:24.422343+00	8	b@gmail.com	1	[{"added": {}}]	6	2
41	2025-08-13 23:39:07.814846+00	8	b@gmail.com	2	[]	6	2
42	2025-08-13 23:40:40.611698+00	9	jeny@gmail.com	1	[{"added": {}}]	6	2
43	2025-08-13 23:41:36.563193+00	9	jeny@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
44	2025-08-13 23:55:17.479631+00	9	jeny@gmail.com	2	[{"changed": {"fields": ["Role"]}}]	6	2
45	2025-08-14 13:44:55.529773+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
46	2025-08-14 14:00:31.311529+00	8	b@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
47	2025-08-14 16:16:36.865917+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
48	2025-08-15 11:34:36.455304+00	10	Mathématiques - Grandeurs et Mesures	1	[{"added": {}}]	23	2
49	2025-08-15 11:36:43.527257+00	11	Mathématiques - Espace et Géométrie	1	[{"added": {}}]	23	2
50	2025-08-15 12:00:14.955605+00	11	Mathématiques - Espace et Géométrie	2	[{"changed": {"fields": ["Ordre"]}}]	23	2
51	2025-08-15 12:00:15.126274+00	10	Mathématiques - Grandeurs et Mesures	2	[{"changed": {"fields": ["Ordre"]}}]	23	2
52	2025-08-15 12:00:43.943393+00	12	Mathématiques - Nombres	1	[{"added": {}}]	23	2
53	2025-08-15 13:29:00.3926+00	12	Mathématiques - Nombres	2	[{"changed": {"fields": ["Ordre"]}}]	23	2
54	2025-08-15 13:29:37.608502+00	13	Mathématiques - Calculs	1	[{"added": {}}]	23	2
55	2025-08-15 13:29:49.772252+00	13	Mathématiques - Calculs	2	[{"changed": {"fields": ["Ordre"]}}]	23	2
56	2025-08-15 14:48:57.279533+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Civilite", "Num\\u00e9ro de t\\u00e9l\\u00e9phone", "Pays", "Niveau pays"]}}]	6	2
57	2025-08-18 14:00:55.719842+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
58	2025-08-22 10:05:38.680694+00	9	jeny@gmail.com	2	[]	6	2
59	2025-08-22 10:05:54.539393+00	7	a@gmail.cpm	2	[{"changed": {"fields": ["Niveau pays", "Is active"]}}]	6	2
60	2025-08-22 10:12:37.885792+00	10	anthonytabet888@gmail.com	1	[{"added": {}}]	6	2
61	2025-08-22 10:13:03.601116+00	10	anthonytabet888@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
62	2025-08-22 10:13:17.22526+00	10	anthonytabet888@gmail.com	2	[{"changed": {"fields": ["Points d'exp\\u00e9rience"]}}]	6	2
63	2025-08-22 10:16:38.221572+00	10	anthonytabet888@gmail.com	2	[{"changed": {"fields": ["First name", "Last name"]}}]	6	2
64	2025-08-22 10:19:45.041872+00	8	b@gmail.com	2	[{"changed": {"fields": ["Civilite", "Points d'exp\\u00e9rience"]}}]	6	2
65	2025-08-22 10:20:20.275627+00	7	a@gmail.cpm	2	[{"changed": {"fields": ["First name", "Last name"]}}]	6	2
66	2025-08-22 10:21:00.784985+00	7	a@gmail.cpm	2	[{"changed": {"fields": ["Points d'exp\\u00e9rience"]}}]	6	2
67	2025-08-22 10:22:01.123903+00	11	aaa@gmail.com	1	[{"added": {}}]	6	2
68	2025-08-22 10:22:17.12195+00	11	aaa@gmail.com	2	[{"changed": {"fields": ["Civilite", "Pays", "Niveau pays", "Points d'exp\\u00e9rience"]}}]	6	2
69	2025-08-22 10:22:45.95792+00	11	aaa@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
70	2025-08-22 10:24:26.714108+00	12	an@gmail.com	1	[{"added": {}}]	6	2
71	2025-08-22 10:24:44.122564+00	12	an@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays", "Points d'exp\\u00e9rience", "Is active"]}}]	6	2
72	2025-08-31 08:51:23.972235+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
73	2025-09-03 14:40:56.710066+00	13	Krista@gmail.com	1	[{"added": {}}]	6	2
74	2025-09-03 14:41:48.949822+00	13	Krista@gmail.com	2	[{"changed": {"fields": ["Civilite", "Is active"]}}]	6	2
75	2025-09-03 15:01:37.387026+00	9	jeny@gmail.com	2	[{"changed": {"fields": ["Role", "Is staff"]}}]	6	2
76	2025-09-09 10:05:01.435515+00	14	karen@gmail.com	1	[{"added": {}}]	6	2
77	2025-09-09 10:05:13.82117+00	14	karen@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
78	2025-09-09 19:06:14.810603+00	15	karenchahwan@gmail.com	1	[{"added": {}}]	6	2
79	2025-09-09 19:06:27.62776+00	15	karenchahwan@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
80	2025-09-09 19:06:43.762721+00	15	karenchahwan@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
81	2025-09-11 14:43:33.15916+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Date de naissance"]}}]	6	2
82	2025-09-14 16:50:27.108626+00	33	Mathématiques - Algèbre	1	[{"added": {}}]	23	2
83	2025-09-14 18:26:01.621347+00	16	chahwanjenny@gmail.com	1	[{"added": {}}]	6	2
84	2025-09-14 18:26:26.650005+00	16	chahwanjenny@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
85	2025-09-15 07:17:41.823294+00	1	Password reset token for user anthonytabet.c@gmail.com	2	[]	9	2
86	2025-09-15 09:41:31.686433+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Pays", "Niveau pays"]}}]	6	2
87	2025-09-15 09:47:33.748176+00	17	tabet.lmnp@gmail.com	3		6	2
88	2025-09-15 10:02:20.873508+00	19	tabet.lmnp@gmail.com	2	[{"changed": {"fields": ["Is active"]}}]	6	2
89	2025-09-15 10:15:06.515436+00	19	tabet.lmnp@gmail.com	3		6	2
90	2025-09-15 10:19:22.821623+00	20	tabet.lmnp@gmail.com	3		6	2
91	2025-09-15 10:21:32.789789+00	21	tabet.lmnp@gmail.com	3		6	2
92	2025-09-15 10:26:00.20348+00	22	tabet.lmnp@gmail.com	3		6	2
93	2025-09-15 10:30:53.144002+00	23	tabet.lmnp@gmail.com	3		6	2
94	2025-09-15 10:34:12.70705+00	24	tabet.lmnp@gmail.com	3		6	2
95	2025-09-15 11:35:12.166062+00	27	tabet.lmnp444@gmail.com	3		6	2
96	2025-09-15 11:35:12.166143+00	26	anthonytabet88858@gmail.com	3		6	2
97	2025-09-15 11:35:12.166191+00	25	tabet.lmnp@gmail.com	3		6	2
98	2025-09-15 11:38:16.144504+00	28	tabet.lmnp@gmail.com	3		6	2
99	2025-09-15 11:38:16.144576+00	18	anthonytabet8858@gmail.com	3		6	2
100	2025-09-15 12:08:19.224281+00	29	tabet.lmnp@gmail.com	3		6	2
101	2025-09-15 12:22:34.77883+00	30	tabet.lmnp@gmail.com	3		6	2
102	2025-09-15 12:30:56.722671+00	31	tabet.lmnp@gmail.com	3		6	2
103	2025-09-15 12:34:44.582757+00	32	tabet.lmnp@gmail.com	3		6	2
104	2025-09-15 12:45:37.660777+00	33	tabet.lmnp@gmail.com	3		6	2
105	2025-09-15 12:50:24.856707+00	34	tabet.lmnp@gmail.com	3		6	2
106	2025-09-15 13:22:28.196753+00	92	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 19testtsttststtststs	3		19	2
107	2025-09-15 13:22:28.196808+00	90	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 41	3		19	2
108	2025-09-15 13:22:28.196831+00	89	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 40	3		19	2
109	2025-09-15 13:22:28.19685+00	88	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 39	3		19	2
110	2025-09-15 13:22:28.196868+00	87	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 38	3		19	2
111	2025-09-15 13:22:28.196887+00	86	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 37	3		19	2
112	2025-09-15 13:22:28.196904+00	85	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 36	3		19	2
113	2025-09-15 13:22:28.196921+00	84	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 35	3		19	2
114	2025-09-15 13:22:28.196938+00	83	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 34	3		19	2
115	2025-09-15 13:22:28.196955+00	82	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 33	3		19	2
116	2025-09-15 13:22:28.196974+00	81	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Moyen 32	3		19	2
117	2025-09-15 13:22:28.196991+00	80	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Difficile 31	3		19	2
118	2025-09-15 13:22:28.197007+00	79	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Difficile 30	3		19	2
119	2025-09-15 13:22:28.197024+00	78	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Difficile 29	3		19	2
120	2025-09-15 13:22:28.197041+00	77	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Difficile 28	3		19	2
121	2025-09-15 13:22:28.197058+00	76	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Difficile 27	3		19	2
122	2025-09-15 13:22:28.197076+00	75	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 10	3		19	2
123	2025-09-15 13:22:28.197096+00	74	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 9	3		19	2
124	2025-09-15 13:22:28.197115+00	73	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 8	3		19	2
125	2025-09-15 13:22:28.197132+00	72	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 7	3		19	2
126	2025-09-15 13:22:28.197148+00	71	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 6	3		19	2
127	2025-09-15 13:22:28.197162+00	70	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 5	3		19	2
128	2025-09-15 13:22:28.197177+00	69	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Facile 4	3		19	2
129	2025-09-15 13:22:28.197192+00	68	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Simple 3	3		19	2
130	2025-09-15 13:22:28.197207+00	67	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Simple 2	3		19	2
131	2025-09-15 13:22:28.197238+00	66	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Simple 1	3		19	2
132	2025-09-15 13:22:28.197253+00	65	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 26	3		19	2
133	2025-09-15 13:22:28.197268+00	64	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 25	3		19	2
134	2025-09-15 13:22:28.197283+00	63	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 24	3		19	2
190	2025-09-15 13:26:57.675029+00	171	Chapitre 3: Suites Géométriques - Application à la physique	3		26	2
135	2025-09-15 13:22:28.197299+00	62	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 23	3		19	2
136	2025-09-15 13:22:28.197314+00	61	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 22	3		19	2
137	2025-09-15 13:22:28.197329+00	60	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 21	3		19	2
138	2025-09-15 13:22:28.197354+00	59	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 20	3		19	2
139	2025-09-15 13:22:28.197369+00	58	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 19	3		19	2
140	2025-09-15 13:22:28.197384+00	57	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 18	3		19	2
141	2025-09-15 13:22:28.197399+00	56	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 17	3		19	2
142	2025-09-15 13:22:28.197414+00	55	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 16	3		19	2
143	2025-09-15 13:22:28.197429+00	54	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 15	3		19	2
144	2025-09-15 13:22:28.197444+00	53	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 14	3		19	2
145	2025-09-15 13:22:28.19746+00	52	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 13	3		19	2
146	2025-09-15 13:22:28.197489+00	51	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 12	3		19	2
147	2025-09-15 13:22:28.197505+00	50	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 11	3		19	2
148	2025-09-15 13:22:28.19752+00	49	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 10	3		19	2
149	2025-09-15 13:22:28.197535+00	48	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 9	3		19	2
150	2025-09-15 13:22:28.19755+00	47	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 8	3		19	2
151	2025-09-15 13:22:28.197565+00	46	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 7	3		19	2
152	2025-09-15 13:22:28.197581+00	45	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 6	3		19	2
153	2025-09-15 13:22:28.197596+00	44	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 5	3		19	2
154	2025-09-15 13:22:28.197611+00	43	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 4	3		19	2
155	2025-09-15 13:22:28.197627+00	42	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 3	3		19	2
156	2025-09-15 13:22:28.197643+00	41	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 2	3		19	2
157	2025-09-15 13:22:28.197664+00	40	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Limites - Niveau 1	3		19	2
158	2025-09-15 13:22:28.197681+00	39	Quiz - Chapitre 1: Introduction aux Limites et Intuition - Quiz Croissances comparées	3		19	2
159	2025-09-15 13:22:28.197697+00	91	Quiz - Chapitre 4: Les Croissances Comparées - ddddd	3		19	2
160	2025-09-15 13:26:57.674022+00	150	Chapitre 2: Suites Arithmétiques - Calcul de la raison	3		26	2
161	2025-09-15 13:26:57.674098+00	124	Chapitre 2: Suites Arithmétiques - Calcul de la somme des premiers termes	3		26	2
162	2025-09-15 13:26:57.674136+00	127	Chapitre 2: Suites Arithmétiques - Calcul d'un terme particulier avec paramètres complexes	3		26	2
163	2025-09-15 13:26:57.674167+00	122	Chapitre 2: Suites Arithmétiques - Calcul du terme général d'une suite arithmétique	3		26	2
164	2025-09-15 13:26:57.674196+00	147	Chapitre 2: Suites Arithmétiques - Calcul simple du terme général	3		26	2
165	2025-09-15 13:26:57.674226+00	131	Chapitre 2: Suites Arithmétiques - Comparaison de sommes de suites arithmétiques	3		26	2
166	2025-09-15 13:26:57.674256+00	123	Chapitre 2: Suites Arithmétiques - Détermination de la raison d'une suite arithmétique	3		26	2
167	2025-09-15 13:26:57.674285+00	126	Chapitre 2: Suites Arithmétiques - Problème concret avec suite arithmétique	3		26	2
168	2025-09-15 13:26:57.674313+00	149	Chapitre 2: Suites Arithmétiques - Problème concret simple	3		26	2
169	2025-09-15 13:26:57.674343+00	136	Chapitre 2: Suites Arithmétiques - Problème de convergence et terme général	3		26	2
170	2025-09-15 13:26:57.674373+00	140	Chapitre 2: Suites Arithmétiques - Problème d'épargne avec suite arithmétique	3		26	2
171	2025-09-15 13:26:57.674402+00	138	Chapitre 2: Suites Arithmétiques - Problème de progression arithmétique dans un triangle	3		26	2
172	2025-09-15 13:26:57.67443+00	145	Chapitre 2: Suites Arithmétiques - Problème d'intersection de suites arithmétiques	3		26	2
173	2025-09-15 13:26:57.674459+00	134	Chapitre 2: Suites Arithmétiques - Problème d'optimisation avec contraintes	3		26	2
174	2025-09-15 13:26:57.674487+00	129	Chapitre 2: Suites Arithmétiques - Problème d'optimisation avec suite arithmétique	3		26	2
175	2025-09-15 13:26:57.674516+00	125	Chapitre 2: Suites Arithmétiques - Reconnaissance d'une suite arithmétique	3		26	2
176	2025-09-15 13:26:57.674546+00	133	Chapitre 2: Suites Arithmétiques - Somme alternée de termes d'une suite arithmétique	3		26	2
177	2025-09-15 13:26:57.674575+00	148	Chapitre 2: Suites Arithmétiques - Somme des premiers termes	3		26	2
178	2025-09-15 13:26:57.674679+00	128	Chapitre 2: Suites Arithmétiques - Somme de termes avec indice variable	3		26	2
179	2025-09-15 13:26:57.67471+00	142	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec condition d'égalité	3		26	2
180	2025-09-15 13:26:57.674739+00	146	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec propriété fonctionnelle	3		26	2
181	2025-09-15 13:26:57.674769+00	144	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec racine carrée	3		26	2
182	2025-09-15 13:26:57.674797+00	141	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec terme central	3		26	2
183	2025-09-15 13:26:57.674826+00	132	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec terme en fonction d'un paramètre	3		26	2
184	2025-09-15 13:26:57.674854+00	130	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec terme nul	3		26	2
185	2025-09-15 13:26:57.674883+00	135	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec terme nul et positivité	3		26	2
186	2025-09-15 13:26:57.674912+00	137	Chapitre 2: Suites Arithmétiques - Suite arithmétique avec termes donnés	3		26	2
187	2025-09-15 13:26:57.674942+00	151	Chapitre 2: Suites Arithmétiques - Suite arithmétique et moyenne	3		26	2
188	2025-09-15 13:26:57.674971+00	139	Chapitre 2: Suites Arithmétiques - Suite arithmétique et moyenne arithmétique	3		26	2
189	2025-09-15 13:26:57.674999+00	143	Chapitre 2: Suites Arithmétiques - Système complexe avec deux suites arithmétiques	3		26	2
191	2025-09-15 13:26:57.675058+00	161	Chapitre 3: Suites Géométriques - Application à l'intérêt composé	3		26	2
192	2025-09-15 13:26:57.675086+00	157	Chapitre 3: Suites Géométriques - Calcul de terme particulier	3		26	2
193	2025-09-15 13:26:57.675115+00	152	Chapitre 3: Suites Géométriques - Calcul du terme général simple	3		26	2
194	2025-09-15 13:26:57.675143+00	169	Chapitre 3: Suites Géométriques - Comparaison de sommes partielles	3		26	2
195	2025-09-15 13:26:57.675172+00	159	Chapitre 3: Suites Géométriques - Comparaison de termes	3		26	2
196	2025-09-15 13:26:57.6752+00	153	Chapitre 3: Suites Géométriques - Détermination de la raison	3		26	2
197	2025-09-15 13:26:57.675228+00	179	Chapitre 3: Suites Géométriques - Étude de convergence d'une suite géométrique	3		26	2
198	2025-09-15 13:26:57.675256+00	181	Chapitre 3: Suites Géométriques - Exercice 1 - Étude d'une suite géométrique et résolution d'une inéquation	3		26	2
199	2025-09-15 13:26:57.675285+00	180	Chapitre 3: Suites Géométriques - Problème concret avec progression géométrique	3		26	2
200	2025-09-15 13:26:57.675315+00	156	Chapitre 3: Suites Géométriques - Problème concret simple	3		26	2
201	2025-09-15 13:26:57.675344+00	167	Chapitre 3: Suites Géométriques - Problème de convergence	3		26	2
202	2025-09-15 13:26:57.675372+00	176	Chapitre 3: Suites Géométriques - Problème de maximum pour une suite géométrique	3		26	2
203	2025-09-15 13:26:57.675401+00	164	Chapitre 3: Suites Géométriques - Problème d'épargne géométrique	3		26	2
204	2025-09-15 13:26:57.675429+00	177	Chapitre 3: Suites Géométriques - Problème de triangulation avec suite géométrique	3		26	2
205	2025-09-15 13:26:57.675458+00	173	Chapitre 3: Suites Géométriques - Problème d'optimisation financière	3		26	2
206	2025-09-15 13:26:57.675487+00	178	Chapitre 3: Suites Géométriques - Propriétés des termes d'une suite géométrique	3		26	2
207	2025-09-15 13:26:57.675515+00	155	Chapitre 3: Suites Géométriques - Reconnaissance d'une suite géométrique	3		26	2
208	2025-09-15 13:26:57.675544+00	163	Chapitre 3: Suites Géométriques - Somme avec raison fractionnaire	3		26	2
209	2025-09-15 13:26:57.675572+00	154	Chapitre 3: Suites Géométriques - Somme des premiers termes	3		26	2
210	2025-09-15 13:26:57.6756+00	166	Chapitre 3: Suites Géométriques - Somme de termes spécifiques	3		26	2
211	2025-09-15 13:26:57.675634+00	175	Chapitre 3: Suites Géométriques - Somme infinie avec condition	3		26	2
212	2025-09-15 13:26:57.675666+00	160	Chapitre 3: Suites Géométriques - Suite géométrique avec fractions	3		26	2
213	2025-09-15 13:26:57.675696+00	170	Chapitre 3: Suites Géométriques - Suite géométrique avec logarithmes	3		26	2
214	2025-09-15 13:26:57.675726+00	174	Chapitre 3: Suites Géométriques - Suite géométrique avec terme en fonction d'un paramètre	3		26	2
215	2025-09-15 13:26:57.675754+00	168	Chapitre 3: Suites Géométriques - Suite géométrique avec terme nul	3		26	2
216	2025-09-15 13:26:57.675783+00	162	Chapitre 3: Suites Géométriques - Suite géométrique avec termes donnés	3		26	2
217	2025-09-15 13:26:57.67581+00	158	Chapitre 3: Suites Géométriques - Suite géométrique décroissante	3		26	2
218	2025-09-15 13:26:57.675843+00	165	Chapitre 3: Suites Géométriques - Suite géométrique et équation	3		26	2
219	2025-09-15 13:26:57.675872+00	172	Chapitre 3: Suites Géométriques - Système complexe avec deux suites géométriques	3		26	2
220	2025-09-17 20:46:29.594489+00	2	anthonytabet.c@gmail.com	2	[]	6	2
221	2025-09-17 21:05:36.194053+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Streak (jours)"]}}]	6	2
222	2025-09-17 21:06:23.664011+00	2	anthonytabet.c@gmail.com	2	[{"changed": {"fields": ["Streak (jours)"]}}]	6	2
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	users	customuser
7	users	userfavoritematiere
8	users	userselectedmatiere
9	django_rest_passwordreset	resetpasswordtoken
10	exercices	notion
11	exercices	matiere
12	exercices	chapitre
13	exercices	theme
14	exercices	exercice
15	cours	cours
16	suivis	suiviquiz
17	suivis	suiviexercice
18	fiches	fichesynthese
19	quiz	quiz
20	pays	pays
22	curriculum	matiere
23	curriculum	theme
24	curriculum	notion
25	curriculum	chapitre
26	curriculum	exercice
21	pays	niveau
27	curriculum	matierecontexte
28	curriculum	exerciceimage
29	users	parentchild
30	synthesis	synthesissheet
31	quiz	quizimage
32	users	usernotification
33	cours	coursimage
34	authtoken	token
35	authtoken	tokenproxy
36	account	emailaddress
37	account	emailconfirmation
38	socialaccount	socialaccount
39	socialaccount	socialapp
40	socialaccount	socialtoken
41	ai	aiconversation
42	users	userdailystreak
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	pays	0001_initial	2025-08-09 14:52:21.114524+00
2	exercices	0001_initial	2025-08-09 14:52:21.399821+00
3	contenttypes	0001_initial	2025-08-09 14:52:21.441949+00
4	contenttypes	0002_remove_content_type_name	2025-08-09 14:52:21.500579+00
5	auth	0001_initial	2025-08-09 14:52:21.681876+00
6	auth	0002_alter_permission_name_max_length	2025-08-09 14:52:21.715958+00
7	auth	0003_alter_user_email_max_length	2025-08-09 14:52:21.742162+00
8	auth	0004_alter_user_username_opts	2025-08-09 14:52:21.779571+00
9	auth	0005_alter_user_last_login_null	2025-08-09 14:52:21.813602+00
10	auth	0006_require_contenttypes_0002	2025-08-09 14:52:21.842565+00
11	auth	0007_alter_validators_add_error_messages	2025-08-09 14:52:21.877528+00
12	auth	0008_alter_user_username_max_length	2025-08-09 14:52:21.912809+00
13	auth	0009_alter_user_last_name_max_length	2025-08-09 14:52:21.945177+00
14	auth	0010_alter_group_name_max_length	2025-08-09 14:52:21.997785+00
15	auth	0011_update_proxy_permissions	2025-08-09 14:52:22.029363+00
16	auth	0012_alter_user_first_name_max_length	2025-08-09 14:52:22.066204+00
17	users	0001_initial	2025-08-09 14:52:22.480824+00
18	admin	0001_initial	2025-08-09 14:52:22.582738+00
19	admin	0002_logentry_remove_auto_add	2025-08-09 14:52:22.608454+00
20	admin	0003_logentry_add_action_flag_choices	2025-08-09 14:52:22.652258+00
21	cours	0001_initial	2025-08-09 14:52:22.704824+00
22	cours	0002_initial	2025-08-09 14:52:22.762901+00
23	django_rest_passwordreset	0001_initial	2025-08-09 14:52:22.860669+00
24	django_rest_passwordreset	0002_pk_migration	2025-08-09 14:52:22.988335+00
25	django_rest_passwordreset	0003_allow_blank_and_null_fields	2025-08-09 14:52:23.058581+00
26	django_rest_passwordreset	0004_alter_resetpasswordtoken_user_agent	2025-08-09 14:52:23.108985+00
27	fiches	0001_initial	2025-08-09 14:52:23.197398+00
28	quiz	0001_initial	2025-08-09 14:52:23.281532+00
29	sessions	0001_initial	2025-08-09 14:52:23.345103+00
30	suivis	0001_initial	2025-08-09 14:52:23.439559+00
31	suivis	0002_initial	2025-08-09 14:52:23.64046+00
32	curriculum	0001_initial	2025-08-09 17:57:43.82294+00
33	curriculum	0002_remove_pays_from_matiere	2025-08-09 21:31:09.391077+00
34	pays	0002_rename_niveaupays_to_niveau	2025-08-09 21:55:28.681954+00
35	cours	0003_remove_description_fields	2025-08-09 22:22:01.56996+00
36	curriculum	0003_remove_description_fields	2025-08-09 22:22:01.68659+00
37	fiches	0002_remove_description_fields	2025-08-09 22:22:01.730537+00
38	quiz	0002_remove_description_fields	2025-08-09 22:22:01.779693+00
39	cours	0004_alter_cours_contenu_alter_cours_date_creation_and_more	2025-08-11 08:39:35.954707+00
40	curriculum	0004_matiere_description_notion_description_and_more	2025-08-11 08:39:36.215212+00
41	fiches	0003_alter_fichesynthese_date_creation_and_more	2025-08-11 08:39:36.253331+00
42	pays	0003_alter_niveau_date_creation_and_more	2025-08-11 08:39:36.330768+00
43	quiz	0003_alter_quiz_contenu_alter_quiz_date_creation_and_more	2025-08-11 08:39:36.437528+00
44	suivis	0003_alter_suiviexercice_date_creation_and_more	2025-08-11 08:39:36.534638+00
45	users	0002_alter_customuser_options_remove_customuser_civilite_and_more	2025-08-11 08:39:36.718588+00
46	users	0003_customuser_civilite_customuser_date_naissance_and_more	2025-08-11 09:25:12.841614+00
47	curriculum	0005_matiere_niveaux_manytomany	2025-08-11 18:30:25.305223+00
48	curriculum	0006_matiere_pays_manytomany	2025-08-11 18:37:52.095476+00
49	curriculum	0005_clean_matiere_model	2025-08-11 19:07:27.206172+00
50	curriculum	0006_fix_matiere_model	2025-08-11 22:07:55.535148+00
51	curriculum	0007_alter_matiere_unique_together_and_more	2025-08-12 00:06:09.234481+00
52	curriculum	0008_fix_theme_niveaux_table	2025-08-12 00:08:29.262649+00
53	curriculum	0009_notion_niveaux	2025-08-12 03:52:40.457567+00
54	curriculum	0002_matierecontexte_theme_contexte	2025-08-12 20:20:48.998858+00
55	curriculum	0003_remove_matiere_niveaux_remove_matiere_pays_and_more	2025-08-12 20:27:30.58149+00
56	curriculum	0004_exerciceimage	2025-08-13 22:47:26.100314+00
57	users	0002_customuser_xp	2025-08-13 23:17:58.104325+00
58	users	0003_customuser_role_parentchild	2025-08-13 23:49:01.195883+00
59	curriculum	0005_exercice_etapes	2025-08-16 11:34:51.531911+00
60	suivis	0003_suiviquiz_gamification	2025-08-16 16:50:27.808698+00
61	users	0003_reset_xp_levels	2025-08-16 16:50:46.272843+00
62	users	0004_merge_20250816_1849	2025-08-16 16:50:46.277066+00
65	synthesis	0002_auto_20250820_1444	2025-08-20 12:46:29.085358+00
66	synthesis	0001_initial	2025-08-20 12:56:06.652037+00
67	quiz	0002_quizimage	2025-08-24 08:08:55.68788+00
68	users	0005_usernotification	2025-08-24 10:35:50.461099+00
69	cours	0002_coursimage	2025-08-24 11:09:41.300752+00
70	account	0001_initial	2025-09-06 12:59:33.911786+00
71	account	0002_email_max_length	2025-09-06 12:59:33.955515+00
72	account	0003_alter_emailaddress_create_unique_verified_email	2025-09-06 12:59:33.990975+00
73	account	0004_alter_emailaddress_drop_unique_email	2025-09-06 12:59:34.051388+00
74	account	0005_emailaddress_idx_upper_email	2025-09-06 12:59:34.073463+00
75	account	0006_emailaddress_lower	2025-09-06 12:59:34.117775+00
76	account	0007_emailaddress_idx_email	2025-09-06 12:59:34.218426+00
77	account	0008_emailaddress_unique_primary_email_fixup	2025-09-06 12:59:34.255813+00
78	account	0009_emailaddress_unique_primary_email	2025-09-06 12:59:34.273759+00
79	authtoken	0001_initial	2025-09-06 12:59:34.315712+00
80	authtoken	0002_auto_20160226_1747	2025-09-06 12:59:34.392575+00
81	authtoken	0003_tokenproxy	2025-09-06 12:59:34.397115+00
82	authtoken	0004_alter_tokenproxy_options	2025-09-06 12:59:34.40421+00
83	socialaccount	0001_initial	2025-09-06 12:59:34.517362+00
84	socialaccount	0002_token_max_lengths	2025-09-06 12:59:34.546881+00
85	socialaccount	0003_extra_data_default_dict	2025-09-06 12:59:34.563646+00
86	socialaccount	0004_app_provider_id_settings	2025-09-06 12:59:34.607718+00
87	socialaccount	0005_socialtoken_nullable_app	2025-09-06 12:59:34.652469+00
88	socialaccount	0006_alter_socialaccount_extra_data	2025-09-06 12:59:34.681341+00
89	ai	0001_initial	2025-09-06 21:00:06.686656+00
90	users	0006_optimize_auth_indexes	2025-09-10 06:49:58.171303+00
91	users	0007_remove_customuser_users_custo_email_1a70ed_idx_and_more	2025-09-12 18:48:18.202785+00
92	curriculum	0006_alter_theme_unique_together	2025-09-14 15:40:48.879798+00
93	curriculum	0007_drop_old_unique_matiere_titre	2025-09-14 15:57:34.721409+00
94	users	0008_userdailystreak	2025-09-14 18:32:05.364514+00
95	users	0009_delete_userdailystreak	2025-09-14 21:17:34.271436+00
96	users	0008_customuser_verification_code_sent_at	2025-09-15 09:55:34.066986+00
97	users	0009_customuser_email_verified	2025-09-15 12:45:04.94084+00
98	users	0010_alter_customuser_is_active	2025-09-15 12:45:05.020879+00
99	users	0011_remove_customuser_email_verified_and_more	2025-09-15 12:49:36.215932+00
100	users	0012_customuser_streak	2025-09-17 20:56:12.306102+00
\.


--
-- Data for Name: django_rest_passwordreset_resetpasswordtoken; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.django_rest_passwordreset_resetpasswordtoken (created_at, key, ip_address, user_agent, user_id, id) FROM stdin;
2025-09-15 07:21:41.368656+00	c1f345034ce1e63e597fb2	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36	2	4
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
o7ft1zsewr2bbud3gc8piby1r6kixveg	.eJxVjMsOwiAQRf-FtSEMz8Gle7-BAEOlaiAp7cr479qkC93ec859sRC3tYZtlCXMxM5MstPvlmJ-lLYDusd26zz3ti5z4rvCDzr4tVN5Xg7376DGUb-1lgrMJCVizkoonTQ4LwARhVMTWSNUTI6cddZnGVGAJvDJqAISSQN7fwCdfTYe:1uknRD:2ZlIZ8mgac5pAtOVa0fI3ALJPkQwJTbt9cLgO79haDU	2025-08-23 17:32:59.227883+00
x8m1ug3jsklvn0jnmqy07zfycedkk8vd	.eJxVjMsOwiAQRf-FtSEMz8Gle7-BAEOlaiAp7cr479qkC93ec859sRC3tYZtlCXMxM5MstPvlmJ-lLYDusd26zz3ti5z4rvCDzr4tVN5Xg7376DGUb-1lgrMJCVizkoonTQ4LwARhVMTWSNUTI6cddZnGVGAJvDJqAISSQN7fwCdfTYe:1ulbZM:FBc4c7SD-syBAPaNKI9Pqc7dL7op7alelug0NUt6oQY	2025-08-25 23:04:44.614473+00
ewdr8let5qigowcwwd6z6moous28vpgv	.eJxVjDsOwjAQBe_iGlnxJms7lPQ5Q7Q_cAAlUj4V4u4QKQW0b2bey_W0raXfFpv7Qd3ZgTv9bkzysHEHeqfxNnmZxnUe2O-KP-jiu0nteTncv4NCS_nWrbBkiPHKiZsYARMiVcEIpK0MNQEw5SYIqgY0QEmaOYW2TmZ1re79AeD8N9Y:1unCE5:bNMRE4UfBL2oy1yyfwHydkF7aa6lauM_-d6YnR_CrME	2025-08-30 08:25:21.028496+00
tpgzlertl58610sn8qk6lomu73ajj6j0	.eJxVjE0OwiAYBe_C2hAKWIpL9z1D8_0hVQNJaVfGu2uTLnT7Zua91ATbmqetyTLNrC7KqtPvhkAPKTvgO5Rb1VTLusyod0UftOmxsjyvh_t3kKHlbx1iEhrEWhYhYEuEEYxYRGIM_kyGjB9cj0midy5xx8alTnpL6IIH9f4AL845cA:1uvqty:38jueat0hxJVKha8Tg5RpGpQLdW9flEoWwgzly5fLes	2025-09-23 05:28:22.365924+00
995e5mdro8g4gfswjjcs7vsnxx6p3qjt	.eJxVjDsOwjAQBe_iGlnxJms7lPQ5Q7Q_cAAlUj4V4u4QKQW0b2bey_W0raXfFpv7Qd3ZgTv9bkzysHEHeqfxNnmZxnUe2O-KP-jiu0nteTncv4NCS_nWrbBkiPHKiZsYARMiVcEIpK0MNQEw5SYIqgY0QEmaOYW2TmZ1re79AeD8N9Y:1uvv7L:OFGMf8kpzMi2ocfXYfmkddCO2oMD0ECcwNJuNtFqui0	2025-09-23 09:58:27.430148+00
rc20jfyx6cfw1krh3sopizsr6zii8izt	.eJxVjMEOwiAQRP-FsyHbxQL16N1vILsLSNXQpLQn47_bJj3ocea9mbcKtC4lrC3NYYzqolCdfjsmeaa6g_igep-0THWZR9a7og_a9G2K6XU93L-DQq1s64xAiaUzFmMPvkvZyJZgYDDWiTifwLizxYF7cdYDejRZMDuxDETq8wXZvTeO:1uxoGn:BcJ7cslT6_PW4XJu4JJCd2d4M1ZLbIt0TZNowYkU9P4	2025-09-28 15:04:01.177235+00
jtg4dj9mmh9ch0133qdkh6089d3j6u3w	.eJxVjMsOwiAQRf-FtSFDeZRx6d5vIMAMUjUlKe3K-O_apAvd3nPOfYkQt7WGrfMSJhJnMYjT75ZifvC8A7rH-dZkbvO6TEnuijxol9dG_Lwc7t9Bjb1-62L9yJ7QMGR0mrRV7IwZzGiR2ANqVIjkbDEACTQwKBhycVjQW8Pi_QG9fzan:1uy5hu:W1bR2b3Or7kL4F1GPKR1hn6KlITA50UlsQcMhsdBMKI	2025-09-29 09:41:10.946539+00
6gc269ruftcd5p00n599188mty1oq4ic	.eJxVjMsOwiAQRf-FtSFDeZRx6d5vIMAMUjUlKe3K-O_apAvd3nPOfYkQt7WGrfMSJhJnMYjT75ZifvC8A7rH-dZkbvO6TEnuijxol9dG_Lwc7t9Bjb1-62L9yJ7QMGR0mrRV7IwZzGiR2ANqVIjkbDEACTQwKBhycVjQW8Pi_QG9fzan:1uyz1F:Lnih-F_cZ9G7tu9n7rGTGdRNMLevmF7mfLd9IZ-edMA	2025-10-01 20:44:49.107364+00
a5q1692di95usem7gbc3ox7ktykl9p58	.eJxVjMsOwiAQRf-FtSFDeZRx6d5vIMAMUjUlKe3K-O_apAvd3nPOfYkQt7WGrfMSJhJnMYjT75ZifvC8A7rH-dZkbvO6TEnuijxol9dG_Lwc7t9Bjb1-62L9yJ7QMGR0mrRV7IwZzGiR2ANqVIjkbDEACTQwKBhycVjQW8Pi_QG9fzan:1uyzFc:4pU9j7qyGlq0MSMlOSONpeqC3URI1S4wTnsXAbyrghw	2025-10-01 20:59:40.085933+00
\.


--
-- Data for Name: fiches_fichesynthese; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.fiches_fichesynthese (id, est_actif, date_creation, date_modification, titre, ordre, contenu_markdown, notion_id) FROM stdin;
\.


--
-- Data for Name: pays_niveau; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.pays_niveau (id, est_actif, date_creation, date_modification, nom, ordre, couleur, pays_id) FROM stdin;
10	t	2025-08-14 22:01:12.231084+00	2025-08-14 22:01:12.231124+00	CE1	1	#3b82f6	1
11	t	2025-08-14 22:01:48.643042+00	2025-08-14 22:02:01.90053+00	CE2	2	#b53bf7	1
12	t	2025-08-14 22:02:24.455776+00	2025-08-14 22:02:49.977951+00	CM1	3	#3bf773	1
13	t	2025-08-14 22:03:18.141169+00	2025-08-14 22:03:18.141203+00	CM2	4	#f7863b	1
14	t	2025-08-14 22:06:02.755202+00	2025-08-14 22:06:33.998628+00	6ème	5	#f73b61	1
15	t	2025-08-14 22:09:29.147384+00	2025-08-14 22:09:29.147417+00	5ème	6	#99f73b	1
16	t	2025-08-14 22:10:19.602757+00	2025-08-15 13:21:07.638997+00	4ème	7	#f73b3b	1
17	t	2025-08-15 13:18:08.252563+00	2025-08-15 13:21:22.567518+00	3ème	8	#cef73b	1
18	t	2025-08-15 13:22:55.607869+00	2025-08-15 13:22:55.607899+00	2nde	9	#802e28	1
19	t	2025-08-15 13:23:19.048491+00	2025-08-15 13:23:19.04852+00	1ère	10	#f43bf7	1
20	t	2025-08-15 13:23:37.953744+00	2025-08-15 13:23:37.953755+00	Terminale	11	#3b82f6	1
\.


--
-- Data for Name: pays_pays; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.pays_pays (id, est_actif, date_creation, date_modification, nom, ordre, code_iso, drapeau_emoji) FROM stdin;
1	t	2024-01-01 00:00:00+00	2024-01-01 00:00:00+00	France	1	FR	🇫🇷
2	t	2025-08-10 10:54:35.854292+00	2025-08-10 10:54:35.854319+00	Lebanon	2	LB	LB
\.


--
-- Data for Name: quiz_quiz; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.quiz_quiz (id, est_actif, date_creation, date_modification, titre, ordre, contenu, difficulty, questions_data, duree_minutes, chapitre_id) FROM stdin;
94	t	2025-09-17 14:21:33.541162+00	2025-09-17 14:21:33.541178+00	Quiz Dérivées - Niveau 1	0	: Testez vos connaissances sur les dérivées	medium	[{"options": ["$2x$", "$x$", "$2$", "$x^2$"], "question": "Quelle est la dérivée de $f(x) = x^2$ ?", "explanation": "La dérivée de $x^2$ est $2x$ d'après la règle de puissance.", "correct_answer": 0}, {"options": ["$-\\\\cos(x)$", "$\\\\cos(x)$", "$\\\\sin(x)$", "$-\\\\sin(x)$"], "question": "Quelle est la dérivée de $f(x) = \\\\sin(x)$ ?", "explanation": "La dérivée de $\\\\sin(x)$ est $\\\\cos(x)$.", "correct_answer": 1}]	30	22
95	t	2025-09-17 14:21:34.070989+00	2025-09-17 14:21:34.071015+00	Quiz Dérivées - Niveau 2	0	: Quiz intermédiaire sur les dérivées	medium	[{"options": ["$3x^2 + 2$", "$3x^2 + x$", "$x^2 + 2$", "$x^3 + 2$"], "question": "Quelle est la dérivée de $f(x) = x^3 + 2x$ ?", "explanation": "On applique la règle de puissance : $(x^n)' = nx^{n-1}$.", "correct_answer": 0}, {"options": ["$e^x$", "$xe^{x-1}$", "$1$", "$x$"], "question": "Quelle est la dérivée de $f(x) = e^x$ ?", "explanation": "La dérivée de $e^x$ est $e^x$.", "correct_answer": 0}]	30	22
96	t	2025-09-17 14:21:34.81918+00	2025-09-17 14:21:34.819213+00	Quiz Intégrales - Niveau 1	0	: Quiz sur les intégrales simples	easy	[{"options": ["$\\\\frac{x^2}{2} + C$", "$x^2 + C$", "$x + C$", "$\\\\ln(x) + C$"], "question": "Quelle est l'intégrale de $f(x) = x$ ?", "explanation": "$\\\\int x dx = \\\\frac{x^2}{2} + C$.", "correct_answer": 0}, {"options": ["$x + C$", "$1 + C$", "$0$", "$\\\\frac{1}{2} x^2 + C$"], "question": "Quelle est l'intégrale de $f(x) = 1$ ?", "explanation": "L'intégrale de 1 est $x + C$.", "correct_answer": 0}]	30	22
97	t	2025-09-17 14:21:35.446365+00	2025-09-17 14:21:35.446376+00	Quiz Intégrales - Niveau 2	0	: Intégrales un peu plus complexes	medium	[{"options": ["$x^2 + C$", "$x + C$", "$2x + C$", "$x^2/2 + C$"], "question": "Quelle est l'intégrale de $f(x) = 2x$ ?", "explanation": "$\\\\int 2x dx = x^2 + C$.", "correct_answer": 0}, {"options": ["$\\\\sin(x) + C$", "$-\\\\sin(x) + C$", "$\\\\cos(x) + C$", "$-\\\\cos(x) + C$"], "question": "Quelle est l'intégrale de $f(x) = \\\\cos(x)$ ?", "explanation": "$\\\\int \\\\cos(x) dx = \\\\sin(x) + C$.", "correct_answer": 0}]	30	22
98	t	2025-09-17 14:21:36.034271+00	2025-09-17 14:21:36.034294+00	Quiz Fonctions - Niveau 1	0	: Quiz sur les fonctions et leurs propriétés	easy	[{"options": ["6", "9", "3", "12"], "question": "Quelle est la valeur de $f(x) = x^2$ pour $x=3$ ?", "explanation": "$f(3) = 3^2 = 9$.", "correct_answer": 1}, {"options": ["Oui", "Non", "Impossible à dire", "Variable selon x"], "question": "La fonction $f(x) = 2x + 1$ est-elle croissante ?", "explanation": "La pente 2 est positive, donc la fonction est croissante.", "correct_answer": 0}]	30	22
99	t	2025-09-17 14:21:36.601717+00	2025-09-17 14:21:36.601742+00	Quiz Algèbre - Niveau 1	0	: Résolvez des équations simples	easy	[{"options": ["$x = 4$", "$x = 2$", "$x = 8$", "$x = 16$"], "question": "Résoudre $2x = 8$.", "explanation": "$2x = 8 \\\\Rightarrow x = 8/2 = 4$.", "correct_answer": 0}, {"options": ["$x = 7$", "$x = 5$", "$x = 12$", "$x = 17$"], "question": "Résoudre $x + 5 = 12$.", "explanation": "$x = 12 - 5 = 7$.", "correct_answer": 0}]	30	22
100	t	2025-09-17 14:21:38.348366+00	2025-09-17 14:21:38.348387+00	Quiz Algèbre - Niveau 2	0	: Équations un peu plus complexes	medium	[{"options": ["$x = 5$", "$x = 15$", "$x = 7$", "$x = 11$"], "question": "Résoudre $3x - 4 = 11$.", "explanation": "$3x = 15 \\\\Rightarrow x = 5$.", "correct_answer": 0}, {"options": ["$x = 3$", "$x = 5$", "$x = 4$", "$x = 15$"], "question": "Résoudre $5x + 2 = 17$.", "explanation": "$5x = 15 \\\\Rightarrow x = 3$.", "correct_answer": 0}]	30	22
101	t	2025-09-17 14:21:39.106213+00	2025-09-17 14:21:39.106223+00	Quiz Trigonométrie - Niveau 1	0	: Quiz sur les fonctions trigonométriques	medium	[{"options": ["1", "0", "-1", "$\\\\pi/2$"], "question": "Quelle est la valeur de $\\\\sin(\\\\pi/2)$ ?", "explanation": "$\\\\sin(\\\\pi/2) = 1$.", "correct_answer": 0}, {"options": ["0", "1", "-1", "$\\\\pi$"], "question": "Quelle est la valeur de $\\\\cos(0)$ ?", "explanation": "$\\\\cos(0) = 1$.", "correct_answer": 1}]	30	22
102	t	2025-09-17 14:21:39.751196+00	2025-09-17 14:21:39.751211+00	Quiz Limites - Niveau 1	0	: Quiz sur les limites de fonctions simples	medium	[{"options": ["0", "1", "$\\\\infty$", "-1"], "question": "Calculer $\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin(x)}{x}$.", "explanation": "$\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin(x)}{x} = 1$.", "correct_answer": 1}, {"options": ["0", "1", "$\\\\infty$", "-1"], "question": "Calculer $\\\\lim_{x \\\\to \\\\infty} \\\\frac{1}{x}$.", "explanation": "Lorsque x tend vers l’infini, 1/x tend vers 0.", "correct_answer": 0}]	30	22
103	t	2025-09-17 14:21:40.333732+00	2025-09-17 14:21:40.333756+00	Quiz Suites - Niveau 1	0	: Quiz sur les suites numériques	medium	[{"options": ["10", "12", "9", "16"], "question": "Quel est le terme suivant de la suite 2, 4, 6, 8, ... ?", "explanation": "La suite augmente de 2 à chaque terme, donc le suivant est 10.", "correct_answer": 0}, {"options": ["3", "6", "9", "12"], "question": "La suite $u_n = n^2$ pour $n=3$ vaut ?", "explanation": "$u_3 = 3^2 = 9$.", "correct_answer": 2}]	30	22
\.


--
-- Data for Name: quiz_quizimage; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.quiz_quizimage (id, image, image_type, "position", legende, date_creation, date_modification, quiz_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
1	google	100795425661125942484	2025-09-16 05:51:00.677576+00	2025-09-16 05:51:00.677595+00	{"aud": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "azp": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "exp": 1758005457, "iat": 1758001857, "iss": "https://accounts.google.com", "jti": "8ec95525a1c84aefc89e43ed939c7c046e625c9d", "nbf": 1758001557, "sub": "100795425661125942484", "name": "Anthony Tabet", "email": "anthonytabet8858@gmail.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocIuHcrSyz84RwDQqEFvZ40EFlZZaJcfNUeNcRRnD7MSrAM5TA=s96-c", "given_name": "Anthony", "family_name": "Tabet", "email_verified": true}	36
2	google	105578326555548291591	2025-09-16 05:55:11.173352+00	2025-09-16 05:55:11.173371+00	{"aud": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "azp": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "exp": 1758005708, "iat": 1758002108, "iss": "https://accounts.google.com", "jti": "2241565a096fa587fe2420664edf2744c9f502de", "nbf": 1758001808, "sub": "105578326555548291591", "name": "Lina Shabo", "email": "linashabo1967@gmail.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocKNC7BLbfkaaVgIZ4ixPh1OYye-kHw0miXMJXq3b_S6rXnGTA=s96-c", "given_name": "Lina", "family_name": "Shabo", "email_verified": true}	37
3	google	107899527439563661223	2025-09-16 06:09:04.754539+00	2025-09-16 06:09:04.754584+00	{"aud": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "azp": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "exp": 1758006541, "iat": 1758002941, "iss": "https://accounts.google.com", "jti": "e9e110192d0ea3d941ca88edcbf3b1be6131a4d6", "nbf": 1758002641, "sub": "107899527439563661223", "name": "Anthony TABET", "email": "tabet.lmnp@gmail.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocIx3QaAWUX9xwLaV8E3JPm-pgXTwxZioz9SDjF_9ClvVwHZdd8=s96-c", "given_name": "Anthony", "family_name": "TABET", "email_verified": true}	35
4	google	109867426272099539564	2025-09-16 06:21:21.206062+00	2025-09-16 06:21:21.206078+00	{"aud": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "azp": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "exp": 1758007278, "iat": 1758003678, "iss": "https://accounts.google.com", "jti": "e21da18231afe461a870d71432002604029a84e3", "nbf": 1758003378, "sub": "109867426272099539564", "name": "Anthony Tabet", "email": "anthonytabet.c@gmail.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocK-4Tumevk9WU4WrhGfnaA5KFyCB4SxR9bhLlSYffewPGA9iUo=s96-c", "given_name": "Anthony", "family_name": "Tabet", "email_verified": true}	2
5	google	105578093908823694290	2025-09-16 07:10:20.059192+00	2025-09-16 07:10:20.059201+00	{"aud": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "azp": "151259305565-a03g822b5qhoaia71gju8hl9cbnu9lp4.apps.googleusercontent.com", "exp": 1758010213, "iat": 1758006613, "iss": "https://accounts.google.com", "jti": "21cb211b4cd37981a2093337d2e6463f58c09e8c", "nbf": 1758006313, "sub": "105578093908823694290", "name": "LINA CHABOU", "email": "linachabou2@gmail.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocKy2o7XvZCFLRAT8eBhURDIE_3N8Ch1nysKro8IpKeGCMBH2g=s96-c", "given_name": "LINA", "family_name": "CHABOU", "email_verified": true}	38
6	google	108045297997917029324	2025-09-16 08:57:33.569031+00	2025-09-16 08:57:33.569045+00	{"hd": "sweelco.com", "sub": "108045297997917029324", "name": "Anthony Tabet", "email": "anthony@sweelco.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocIndmn7lbKrLgRUR8dU11TmyyHrhPVFKm5cu2tVKCaG6NHq0w=s96-c", "given_name": "Anthony", "family_name": "Tabet", "email_verified": true}	39
7	google	116620584426225118975	2025-09-16 09:38:07.937312+00	2025-09-16 09:38:07.937361+00	{"sub": "116620584426225118975", "name": "Karen Chahwan", "email": "karenchahwan@gmail.com", "picture": "https://lh3.googleusercontent.com/a/ACg8ocJ7yF8fndNIz0ShbKqOylWvqdXfMTlNRsDhBXLusP0cMgLYKA=s96-c", "given_name": "Karen", "family_name": "Chahwan", "email_verified": true}	15
\.


--
-- Data for Name: socialaccount_socialapp; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.socialaccount_socialapp (id, provider, name, client_id, secret, key, provider_id, settings) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialtoken; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
\.


--
-- Data for Name: suivis_suiviexercice; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.suivis_suiviexercice (id, est_actif, date_creation, date_modification, reponse_donnee, est_correct, points_obtenus, temps_seconde, exercice_id, user_id) FROM stdin;
288	t	2025-09-17 12:47:48.569236+00	2025-09-17 12:47:48.569276+00	acquired	t	1	0	190	2
289	t	2025-09-17 12:47:51.995366+00	2025-09-17 12:47:51.995383+00	acquired	t	1	0	192	2
290	t	2025-09-17 12:47:54.83515+00	2025-09-17 12:47:54.835165+00	acquired	t	1	0	194	2
291	t	2025-09-17 12:47:56.66102+00	2025-09-17 12:47:56.661034+00	acquired	t	1	0	199	2
292	t	2025-09-17 12:57:38.061031+00	2025-09-17 12:57:38.061047+00	acquired	t	1	0	207	2
293	t	2025-09-17 12:57:40.165537+00	2025-09-17 12:57:40.165562+00	acquired	t	1	0	203	2
294	t	2025-09-17 12:57:41.849732+00	2025-09-17 12:57:41.84975+00	acquired	t	1	0	206	2
295	t	2025-09-17 12:57:43.12513+00	2025-09-17 12:57:43.125153+00	acquired	t	1	0	205	2
296	t	2025-09-17 12:57:44.247149+00	2025-09-17 12:57:44.247168+00	not_acquired	f	0	0	201	2
297	t	2025-09-17 12:57:45.152236+00	2025-09-17 12:57:45.152246+00	acquired	t	1	0	208	2
298	t	2025-09-17 12:57:45.996028+00	2025-09-17 12:57:45.99605+00	not_acquired	f	0	0	200	2
300	t	2025-09-17 12:57:47.35268+00	2025-09-17 12:57:47.352703+00	acquired	t	1	0	202	2
301	t	2025-09-17 12:57:48.441672+00	2025-09-17 12:57:48.4417+00	acquired	t	1	0	204	2
303	t	2025-09-17 12:57:50.317731+00	2025-09-17 12:57:50.317749+00	not_acquired	f	0	0	209	2
304	t	2025-09-17 13:07:36.773689+00	2025-09-17 13:07:36.773704+00	acquired	t	1	0	217	2
305	t	2025-09-17 13:07:38.579924+00	2025-09-17 13:07:38.579945+00	acquired	t	1	0	213	2
306	t	2025-09-17 13:07:40.14327+00	2025-09-17 13:07:40.143294+00	acquired	t	1	0	216	2
308	t	2025-09-17 13:07:45.424565+00	2025-09-17 13:18:29.842357+00	acquired	t	0	0	211	2
307	t	2025-09-17 13:07:43.303629+00	2025-09-17 13:18:40.9792+00	acquired	t	0	0	215	2
309	t	2025-09-17 13:18:43.816106+00	2025-09-17 13:18:43.816127+00	acquired	t	1	0	218	2
311	t	2025-09-17 13:57:43.287985+00	2025-09-17 13:57:43.287998+00	acquired	t	1	0	227	2
312	t	2025-09-17 13:57:45.244012+00	2025-09-17 13:57:45.244021+00	not_acquired	f	0	0	223	2
313	t	2025-09-17 13:57:47.549425+00	2025-09-17 13:57:47.549435+00	acquired	t	1	0	226	2
314	t	2025-09-17 13:57:49.281961+00	2025-09-17 13:57:49.281985+00	not_acquired	f	0	0	225	2
315	t	2025-09-17 13:57:50.228437+00	2025-09-17 13:57:50.228476+00	acquired	t	1	0	221	2
316	t	2025-09-17 13:57:52.07442+00	2025-09-17 13:57:52.074433+00	acquired	t	1	0	228	2
277	t	2025-09-17 12:17:48.187405+00	2025-09-17 17:13:11.863208+00	acquired	t	1	0	188	2
276	t	2025-09-17 12:17:46.695085+00	2025-09-17 12:17:46.695113+00	acquired	t	1	0	187	2
278	t	2025-09-17 12:44:21.970956+00	2025-09-17 12:44:21.970968+00	acquired	t	1	0	197	2
282	t	2025-09-17 12:44:23.756957+00	2025-09-17 12:44:23.756969+00	not_acquired	f	0	0	193	2
283	t	2025-09-17 12:44:28.970282+00	2025-09-17 12:44:28.970294+00	not_acquired	f	0	0	196	2
284	t	2025-09-17 12:44:31.807494+00	2025-09-17 12:44:31.807516+00	acquired	t	1	0	195	2
285	t	2025-09-17 12:44:32.988238+00	2025-09-17 12:44:32.988263+00	not_acquired	f	0	0	191	2
286	t	2025-09-17 12:45:57.697377+00	2025-09-17 12:45:57.697388+00	not_acquired	f	0	0	198	2
\.


--
-- Data for Name: suivis_suiviquiz; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.suivis_suiviquiz (id, est_actif, date_creation, date_modification, score, total_points, temps_total_seconde, quiz_id, user_id, tentative_numero, xp_gagne) FROM stdin;
167	t	2025-09-17 14:21:59.934941+00	2025-09-17 14:21:59.934955+00	1	2	4	94	2	1	3
168	t	2025-09-17 14:22:07.35686+00	2025-09-17 14:22:07.356901+00	1	2	4	96	2	1	2
169	t	2025-09-17 14:22:13.153462+00	2025-09-17 14:22:13.153473+00	1	2	3	97	2	1	3
170	t	2025-09-17 14:22:19.543267+00	2025-09-17 14:22:19.54329+00	0	2	4	100	2	1	1
171	t	2025-09-17 14:22:26.349645+00	2025-09-17 14:22:26.349669+00	1	2	4	98	2	1	2
172	t	2025-09-17 14:22:35.596482+00	2025-09-17 14:22:35.596496+00	1	2	6	101	2	1	3
173	t	2025-09-17 14:22:42.369611+00	2025-09-17 14:22:42.369654+00	0	2	5	99	2	1	1
174	t	2025-09-17 17:14:43.433709+00	2025-09-17 17:14:43.433722+00	1	2	7	99	2	2	0
175	t	2025-09-17 19:23:18.463248+00	2025-09-17 19:23:18.463268+00	0	2	7	99	2	3	0
176	t	2025-09-17 19:28:11.776039+00	2025-09-17 19:28:11.776071+00	0	2	5	101	2	2	0
\.


--
-- Data for Name: synthesis_synthesissheet; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.synthesis_synthesissheet (id, est_actif, date_creation, date_modification, titre, ordre, summary, difficulty, key_points, formulas, examples, reading_time_minutes, notion_id) FROM stdin;
1	t	2025-08-20 12:59:59.618648+00	2025-08-29 07:34:39.901022+00	Limites	1	# Limites des fonctions\n\n## 1) Notations & définitions\n\n- **Limite finie en a** : on écrit $\\displaystyle \\lim_{x \\to a} f(x)=\\ell$ si $f(x)$ peut être rendu aussi proche que l'on veut de $\\ell$ dès que $x$ est assez proche de $a$ (avec $x\\neq a$ si besoin).\n- **Limite infinie** : $\\displaystyle \\lim_{x \\to a} f(x)=+\\infty$ (resp. $-\\infty$) signifie que $f(x)$ devient arbitrairement grand (resp. petit) quand $x$ s'approche de $a$.\n- **Limites à l'infini** : $\\displaystyle \\lim_{x \\to +\\infty} f(x)$, $\\displaystyle \\lim_{x \\to -\\infty} f(x)$.\n- **Limites unilatérales** : $\\displaystyle \\lim_{x \\to a^-} f(x)$ (par la gauche), $\\displaystyle \\lim_{x \\to a^+} f(x)$ (par la droite).\n- **Continuité en a** : $f$ est continue en $a$ si $\\displaystyle \\lim_{x \\to a} f(x)=f(a)$.\n\n## Rappels suites (un)\n\n- $\\displaystyle \\lim_{n \\to +\\infty} u_n=\\ell$ (convergence), ou $+\\infty$, $-\\infty$, ou divergence.\n- **Théorème de la convergence monotone** : si $(u_n)$ est croissante et majorée, alors elle converge (similaire pour décroissante et minorée).\n\n## 2) Règles de calcul de limites (fonctions)\n\nSoient $f$ et $g$ telles que leurs limites existent (finies) en $a$ :\n- **Somme** : $\\displaystyle \\lim (f+g)=\\lim f+\\lim g$\n- **Produit par un réel λ** : $\\displaystyle \\lim (\\lambda f)=\\lambda \\lim f$\n- **Produit** : $\\displaystyle \\lim (fg)=(\\lim f)(\\lim g)$\n- **Quotient** : si $\\lim g\\neq 0$, alors $\\displaystyle \\lim \\tfrac{f}{g}=\\tfrac{\\lim f}{\\lim g}$\n- **Composition** : si $\\displaystyle \\lim_{x \\to a} f(x)=L$ et $g$ est continue en $L$, alors $\\displaystyle \\lim g(f(x))=g(L)$\n\n## ⚠️ Formes indéterminées\n\n$$0\\times \\infty,\\ \\tfrac{0}{0},\\ \\tfrac{\\infty}{\\infty},\\ \\infty-\\infty,\\ 1^{\\infty},\\ 0^{0},\\ \\infty^{0}$$\n\n## 💡 Outils pour lever l'indétermination\n\n- Factorisation, mise au même dénominateur, rationalisation\n- Comparaisons, équivalents, croissances comparées\n- Développements limités de base\n\n## 3) Limites remarquables & équivalents usuels (x → 0)\n\n$$\\displaystyle \\lim_{x \\to 0} \\frac{\\sin x}{x}=1,\\quad \\lim_{x \\to 0} \\frac{e^{x}-1}{x}=1,\\quad \\lim_{x \\to 0} \\frac{\\ln(1+x)}{x}=1$$\n$$\\displaystyle \\lim_{x \\to 0} \\frac{1-\\cos x}{x^{2}}=\\tfrac{1}{2}$$\n\n## Équivalents usuels\n\n- $\\sin x \\sim x$, $\\tan x \\sim x$, $1-\\cos x \\sim \\tfrac{x^{2}}{2}$\n- $e^x - 1 \\sim x$, $\\ln(1+x) \\sim x$\n- $(1+x)^\\alpha \\sim 1+\\alpha x$ ($x\\to 0$, $1+x>0$)\n\n## 4) Croissances comparées (|x|→ +∞)\n\n$$\\ln|x| \\ll x^\\alpha \\ll a^x \\ll x! \\quad (\\alpha>0, a>1)$$\n**Exemple** : $\\displaystyle \\frac{\\ln|x|}{x^\\alpha} \\to 0$ quand $|x|\\to\\infty$\n\n## 5) Asymptotes & comportements limites\n\n- **Horizontale** : $y=\\ell$ si $\\displaystyle \\lim f(x)=\\ell$ en $\\pm\\infty$\n- **Verticale** : $x=a$ si $\\displaystyle \\lim f(x)=\\pm\\infty$\n- **Oblique** : $y=ax+b$ si $\\displaystyle \\lim(f(x)-(ax+b))=0$\n\n## 6) Méthodes classiques de calcul\n\n### A. Factoriser / simplifier\n**Ex** : $\\displaystyle \\lim_{x\\to1}\\frac{x^2-1}{x-1} = 2$\n\n### B. Rationaliser\n**Ex** : $\\displaystyle \\lim_{x\\to0}\\frac{\\sqrt{1+x}-1}{x}=\\tfrac{1}{2}$\n\n### C. Gendarmes\nSi $g(x)\\le f(x)\\le h(x)$ et $\\displaystyle \\lim g=\\lim h=L$, alors $\\lim f=L$\n\n## 7) Suites : limites et outils\n\n- **Géométriques** : $u_{n+1}=q u_n$, si $|q|<1$ alors $\\displaystyle \\lim u_n=0$\n- **Arithmétiques** : $u_n=u_0+nr$, si $r\\ne0$, $|u_n|\\to\\infty$\n- **Par récurrence** : $\\ell=f(\\ell)$, puis vérifier stabilité\n\n**Exemple remarquable** :\n$$\\displaystyle \\lim_{n \\to \\infty}\\left(1+\\tfrac{1}{n}\\right)^n=e$$\n\n## 8) Indéterminations fréquentes\n\n- $\\tfrac{0}{0}$ → factoriser, équivalents\n- $\\tfrac{\\infty}{\\infty}$ → diviser par dominant\n- $\\infty-\\infty$ → regrouper, rationaliser\n- $0\\times\\infty$ → transformer en quotient\n- $1^\\infty$ → passer au $\\ln$\n\n## 9) Tableaux de référence\n\n### A. Limites usuelles (x→0)\n- $\\displaystyle \\tfrac{\\sin x}{x}\\to1$, $\\displaystyle \\tfrac{1-\\cos x}{x^2}\\to \\tfrac{1}{2}$, $\\displaystyle \\tfrac{e^x-1}{x}\\to1$\n\n### B. À l'infini\n- $\\displaystyle \\tfrac{\\ln x}{x^\\alpha}\\to0$, $\\displaystyle \\tfrac{x^n}{e^x}\\to0$, $\\displaystyle \\tfrac{x^n}{x^m}\\to0$ si $n<m$\n\n## 10) Conseils d'examen\n\n1. Identifier le type de limite\n2. Tester la substitution directe\n3. Choisir la bonne stratégie (simplifier, rationaliser, équivalents)\n4. Justifier la méthode (par équivalent, par gendarmes…)\n5. Soigner les asymptotes (calculer $a$, puis $b$)\n\n## ✨ Exemples flash\n\n1. $\\displaystyle \\lim_{x \\to 0}\\tfrac{\\sqrt{1+x}-1}{x}=\\tfrac{1}{2}$\n2. $\\displaystyle \\lim_{x \\to +\\infty}\\tfrac{\\ln x}{x}=0$\n3. $\\displaystyle \\lim_{x \\to +\\infty}\\tfrac{x^2+3x}{e^x}=0$\n4. $\\displaystyle \\lim_{x \\to 0}\\tfrac{\\sin 3x}{x}=3$\n5. **Suite** : $u_{n+1}=\\tfrac{1}{2}u_n+1 \\implies u_n\\to2$	medium	[]	[]	[]	5	20
4	t	2025-09-07 20:06:38.629871+00	2025-09-07 20:06:38.629891+00	suite resumé	1	# Suites numériques — Terminale\n\n## Définition\nUne suite numérique est une fonction définie sur l’ensemble des entiers naturels $\\mathbb{N}$, ou une partie de $\\mathbb{N}$, qui associe à chaque entier $n$ un réel $u_n$, appelé **terme de rang $n$**.  \nOn note souvent $(u_n)$ la suite, et $u_0$, $u_1$, $u_2$, ... ses termes.\n\n## Propriétés importantes\n• Une suite peut être définie :\n   → par une **formule explicite** : $u_n$ est exprimé directement en fonction de $n$.  \n   → par une **relation de récurrence** : $u_{n+1}$ est exprimé en fonction de $u_n$.  \n\n• Une suite peut être :  \n   → **arithmétique** si $u_{n+1} = u_n + r$, où $r$ est la raison.  \n   → **géométrique** si $u_{n+1} = q \\cdot u_n$, où $q$ est la raison.  \n\n• Les suites peuvent être **croissantes**, **décroissantes**, **constantes** ou **monotones**.  \n\n• Les suites ont des **limites** (finies ou infinies), permettant d’étudier leur comportement à l’infini.  \n\n## Formules clés\n- **Suite arithmétique**  \n$$u_n = u_0 + n \\cdot r$$  \n$$S_n = \\frac{(n+1)(u_0 + u_n)}{2}$$ (somme des $n+1$ premiers termes)\n\n- **Suite géométrique**  \n$$u_n = u_0 \\cdot q^n$$  \n$$S_n = u_0 \\cdot \\frac{1 - q^{n+1}}{1 - q} \\quad (q \\neq 1)$$\n\n- **Limites classiques**  \n$$\\lim_{n \\to +\\infty} \\frac{1}{n} = 0$$  \n$$\\lim_{n \\to +\\infty} q^n = 0 \\quad \\text{si } |q| < 1$$  \n$$\\lim_{n \\to +\\infty} q^n = +\\infty \\quad \\text{si } q > 1$$  \n\n## Exemples d'application\nExemple 1 : Suite arithmétique  \nOn considère $(u_n)$ avec $u_0 = 5$ et $r = 3$.  \n→ Formule explicite : $u_n = 5 + 3n$.  \n→ $u_{10} = 5 + 30 = 35$.  \n\nExemple 2 : Suite géométrique  \nOn considère $(v_n)$ avec $v_0 = 2$ et $q = 1,5$.  \n→ Formule explicite : $v_n = 2 \\cdot (1,5)^n$.  \n→ $v_4 = 2 \\cdot (1,5)^4 = 10,125$.  \n\nExemple 3 : Étude d’une limite  \n$(w_n) = \\dfrac{1}{n}$.  \n→ Lorsque $n \\to +\\infty$, $w_n \\to 0$.  \n\n## Points à retenir\n⚠️ Attention :  \n- Ne pas confondre suite arithmétique et géométrique.  \n- Vérifier toujours la valeur initiale $u_0$ ou $u_1$.  \n- Attention aux erreurs de calcul avec les puissances dans les suites géométriques.  \n\n💡 Astuces :  \n- Dans une suite arithmétique, on ajoute toujours la même valeur $r$.  \n- Dans une suite géométrique, on multiplie toujours par le même facteur $q$.  \n- Pour résoudre une inéquation avec une suite géométrique, penser à utiliser les logarithmes.	medium	[]	[]	[]	5	19
7	t	2025-09-14 10:48:54.542954+00	2025-09-14 10:48:54.543059+00	ddddddddd	0	dddddddd	medium	[]	[]	[]	5	17
\.


--
-- Data for Name: users_customuser; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_customuser (id, password, last_login, is_superuser, email, first_name, last_name, is_active, is_staff, verification_code, niveau_pays_id, pays_id, date_joined, civilite, date_naissance, telephone, xp, role, verification_code_sent_at, streak) FROM stdin;
11	pbkdf2_sha256$1000000$doHh86TZTwdTcZ4NKTk6xy$OH58JUpbrfHMwruthUs9YBAs4TCtqNSy0iFl6YgGYI0=	\N	f	aaa@gmail.com	Charbel	Abou	t	f	\N	20	1	2025-08-22 10:22:00+00	M	\N	\N	123	student	\N	0
12	pbkdf2_sha256$1000000$pcoqZBLed4girn5IxPZzrm$0qJeF2dySDEbFM/uYJFHb3eEQJkjNijascsILN2SK6Q=	\N	f	an@gmail.com	Cynthia	Q	t	f	\N	19	1	2025-08-22 10:24:26+00	\N	\N	\N	125	student	\N	0
10	pbkdf2_sha256$1000000$vnH8QKqVR0CnzM6EflMxbg$8bhlfnvRfu03EeA3RMXDgGqcZ25h3H8/6AQ9EO0uKAE=	\N	f	anthonytabet888@gmail.com	Mario	Abou Zeid	t	f	\N	\N	\N	2025-08-22 10:12:35+00	\N	\N	\N	399	student	\N	0
8	pbkdf2_sha256$1000000$5XcKjOLbzeucICESquPTrj$0c07a64TUnb1QzwpYz5TZIEA++eGvlvWvOs82MMN82Q=	\N	f	b@gmail.com	Lina	Chabou	t	f	\N	\N	\N	2025-08-13 23:37:23+00	Mme	\N	\N	221	student	\N	0
13	pbkdf2_sha256$1000000$EhFh5K2ra9rEEUlSuAUyOM$7i8gPa2s/8n2Ee4qi+NoTrgZaRgymTx3JQBRl7ur0ic=	\N	f	krista@gmail.com	Krista	Y	t	f	\N	20	1	2025-09-03 14:40:54+00	Mme	\N	\N	1	student	\N	0
39		\N	f	anthony@sweelco.com	Anthony	Tabet	t	f	\N	20	1	2025-09-16 08:57:33.558699+00	\N	\N	\N	0	student	\N	0
7	pbkdf2_sha256$1000000$L5XaJPH3nx6jMiiEWgNg4W$7Fy1M9rcGl14uFdymE8wMTiLRfeOYqpViJhxBRxlc1c=	\N	f	a@gmail.cpm	Léa	Na	t	f	\N	10	2	2025-08-13 23:36:32+00	Mme	\N	\N	11	student	\N	0
14	pbkdf2_sha256$1000000$5zK2gGFC83mwt492Ae9sum$YI+XM2bcUtwnjR1FPelNBCzME4U+At/riB5tarCPc7o=	\N	f	karen@gmail.com	karen	CHAHWAN	f	f	\N	20	1	2025-09-09 10:05:00+00	\N	\N	\N	0	student	\N	0
9	pbkdf2_sha256$1000000$TfXD2Yid7CpHa5X0ze5arY$IhT63bx6LzjyO7pk+GtTHK42rAVJO5EJF8Se/Id9/+0=	\N	f	jeny@gmail.com	Jenny	CHAHWAN	t	t	\N	20	1	2025-08-13 23:40:39+00	\N	\N	\N	148	student	\N	0
15	pbkdf2_sha256$1000000$u5TmxP8pagI9R99s7P1Aiy$SsWb1LsVwfif2kca/WXdBCm+apwt5ggU8TpRBIIllv0=	\N	f	karenchahwan@gmail.com	karen	CHAHWAN	t	f	\N	20	1	2025-09-09 19:06:14+00	\N	\N	\N	1	student	\N	0
35	pbkdf2_sha256$1000000$23rnYckcEYo9EWDWDqB2w1$rLAQBMrjf9Smi8cvVAo7v3tFoE0T8ACYJwIJhTgxVkI=	\N	f	tabet.lmnp@gmail.com	Anthony	TABET	t	f	\N	20	1	2025-09-15 12:50:35.216831+00	\N	\N	\N	18	student	\N	0
37		\N	f	linashabo1967@gmail.com	Lina	Shabo	t	f	\N	20	1	2025-09-16 05:55:11.163567+00	\N	\N	\N	0	student	\N	0
16	pbkdf2_sha256$1000000$pWRgOUZqtLubbIPE4QQsvN$sYpXjTV2iP+MxnJg5FxU60PFlz1o+Enq4mRfKNXCuuw=	\N	f	chahwanjenny@gmail.com	Jenny	CHAHWAN	t	f	\N	\N	\N	2025-09-14 18:26:01+00	\N	\N	\N	0	student	\N	0
36		\N	f	anthonytabet8858@gmail.com	Anthony	Tabet	t	f	\N	20	1	2025-09-16 05:51:00.653355+00	\N	\N	\N	3	student	\N	0
38		\N	f	linachabou2@gmail.com	LINA	CHABOU	t	f	\N	20	1	2025-09-16 07:10:20.041132+00	\N	\N	\N	0	student	\N	0
2	pbkdf2_sha256$1000000$RSmK6j9qCfvBEkN7qLzlJq$rxV66tQQX+WG/uuEl+gUheNQf6H+iYHgn3l/I5YKJyQ=	2025-09-17 20:59:40+00	t	anthonytabet.c@gmail.com	Anthony	TABET	t	t	\N	20	1	2025-08-11 08:39:36+00	M	1997-08-25	0764040251	735	student	\N	1
\.


--
-- Data for Name: users_customuser_groups; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_customuser_groups (id, customuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: users_parentchild; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_parentchild (id, created_at, child_id, parent_id) FROM stdin;
3	2025-09-01 15:55:28.851251+00	2	9
4	2025-09-12 13:48:54.965311+00	14	2
\.


--
-- Data for Name: users_userfavoritematiere; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_userfavoritematiere (id, created_at, matiere_id, user_id) FROM stdin;
26	2025-09-07 21:18:10.059677+00	7	9
29	2025-09-13 13:35:14.795372+00	1	2
\.


--
-- Data for Name: users_usernotification; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_usernotification (id, type, title, message, data, read, created_at, user_id) FROM stdin;
587	xp_gained	🎉 XP Gagnés !	+2 XP	{"reason": "streak_daily", "xp_delta": 2}	f	2025-09-16 05:51:01.007666+00	36
590	xp_gained	🎉 XP Gagnés !	+1 XP	{"reason": "streak_daily", "xp_delta": 1}	f	2025-09-16 06:35:56.686247+00	36
598	xp_gained	🎉 XP Gagnés !	+1 XP	{"reason": "streak_daily", "xp_delta": 1}	f	2025-09-16 09:42:13.224479+00	15
\.


--
-- Data for Name: users_userselectedmatiere; Type: TABLE DATA; Schema: public; Owner: optitab_db_user
--

COPY public.users_userselectedmatiere (id, "order", is_active, created_at, updated_at, matiere_id, user_id) FROM stdin;
125	0	t	2025-09-16 05:51:09.130963+00	2025-09-16 05:51:09.130977+00	1	36
126	0	t	2025-09-16 05:55:17.670368+00	2025-09-16 05:55:17.670383+00	1	37
40	0	f	2025-08-13 23:57:02.258458+00	2025-08-13 23:57:02.961162+00	1	9
87	0	t	2025-09-07 21:18:08.594883+00	2025-09-07 21:18:08.619146+00	7	9
82	0	t	2025-09-03 14:42:53.794683+00	2025-09-03 14:43:03.951611+00	1	13
127	0	t	2025-09-16 07:10:35.16424+00	2025-09-16 07:10:35.205085+00	1	38
122	0	t	2025-09-15 12:50:49.071629+00	2025-09-16 07:10:52.915547+00	1	35
128	0	t	2025-09-16 08:57:41.994159+00	2025-09-16 08:57:42.922041+00	1	39
129	0	t	2025-09-16 09:42:15.087419+00	2025-09-16 09:42:15.365258+00	1	15
130	0	f	2025-09-17 12:17:12.01048+00	2025-09-17 20:21:48.334385+00	7	2
101	0	t	2025-09-13 13:35:10.261867+00	2025-09-17 20:35:08.076206+00	1	2
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: realtime; Owner: optitab_db_user
--

COPY realtime.schema_migrations (version, inserted_at) FROM stdin;
20211116024918	2025-07-21 09:32:27
20211116045059	2025-07-21 09:32:29
20211116050929	2025-07-21 09:32:31
20211116051442	2025-07-21 09:32:32
20211116212300	2025-07-21 09:32:34
20211116213355	2025-07-21 09:32:36
20211116213934	2025-07-21 09:32:37
20211116214523	2025-07-21 09:32:40
20211122062447	2025-07-21 09:32:41
20211124070109	2025-07-21 09:32:43
20211202204204	2025-07-21 09:32:44
20211202204605	2025-07-21 09:32:46
20211210212804	2025-07-21 09:32:51
20211228014915	2025-07-21 09:32:52
20220107221237	2025-07-21 09:32:54
20220228202821	2025-07-21 09:32:56
20220312004840	2025-07-21 09:32:57
20220603231003	2025-07-21 09:33:00
20220603232444	2025-07-21 09:33:01
20220615214548	2025-07-21 09:33:03
20220712093339	2025-07-21 09:33:05
20220908172859	2025-07-21 09:33:06
20220916233421	2025-07-21 09:33:08
20230119133233	2025-07-21 09:33:09
20230128025114	2025-07-21 09:33:12
20230128025212	2025-07-21 09:33:13
20230227211149	2025-07-21 09:33:15
20230228184745	2025-07-21 09:33:16
20230308225145	2025-07-21 09:33:18
20230328144023	2025-07-21 09:33:19
20231018144023	2025-07-21 09:33:21
20231204144023	2025-07-21 09:33:24
20231204144024	2025-07-21 09:33:25
20231204144025	2025-07-21 09:33:27
20240108234812	2025-07-21 09:33:28
20240109165339	2025-07-21 09:33:30
20240227174441	2025-07-21 09:33:33
20240311171622	2025-07-21 09:33:35
20240321100241	2025-07-21 09:33:38
20240401105812	2025-07-21 09:33:43
20240418121054	2025-07-21 09:33:45
20240523004032	2025-07-21 09:33:51
20240618124746	2025-07-21 09:33:52
20240801235015	2025-07-21 09:33:54
20240805133720	2025-07-21 09:33:55
20240827160934	2025-07-21 09:33:57
20240919163303	2025-07-21 09:33:59
20240919163305	2025-07-21 09:34:01
20241019105805	2025-07-21 09:34:02
20241030150047	2025-07-21 09:34:08
20241108114728	2025-07-21 09:34:10
20241121104152	2025-07-21 09:34:12
20241130184212	2025-07-21 09:34:14
20241220035512	2025-07-21 09:34:15
20241220123912	2025-07-21 09:34:17
20241224161212	2025-07-21 09:34:18
20250107150512	2025-07-21 09:34:20
20250110162412	2025-07-21 09:34:22
20250123174212	2025-07-21 09:34:23
20250128220012	2025-07-21 09:34:25
20250506224012	2025-07-21 09:34:26
20250523164012	2025-07-21 09:34:27
20250714121412	2025-07-21 09:34:29
\.


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: realtime; Owner: optitab_db_user
--

COPY realtime.subscription (id, subscription_id, entity, filters, claims, created_at) FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: optitab_db_user
--

COPY storage.buckets (id, name, owner, created_at, updated_at, public, avif_autodetection, file_size_limit, allowed_mime_types, owner_id) FROM stdin;
\.


--
-- Data for Name: migrations; Type: TABLE DATA; Schema: storage; Owner: optitab_db_user
--

COPY storage.migrations (id, name, hash, executed_at) FROM stdin;
0	create-migrations-table	e18db593bcde2aca2a408c4d1100f6abba2195df	2025-07-21 09:32:23.692857
1	initialmigration	6ab16121fbaa08bbd11b712d05f358f9b555d777	2025-07-21 09:32:23.703322
2	storage-schema	5c7968fd083fcea04050c1b7f6253c9771b99011	2025-07-21 09:32:23.706695
3	pathtoken-column	2cb1b0004b817b29d5b0a971af16bafeede4b70d	2025-07-21 09:32:23.735486
4	add-migrations-rls	427c5b63fe1c5937495d9c635c263ee7a5905058	2025-07-21 09:32:23.750012
5	add-size-functions	79e081a1455b63666c1294a440f8ad4b1e6a7f84	2025-07-21 09:32:23.753678
6	change-column-name-in-get-size	f93f62afdf6613ee5e7e815b30d02dc990201044	2025-07-21 09:32:23.75842
7	add-rls-to-buckets	e7e7f86adbc51049f341dfe8d30256c1abca17aa	2025-07-21 09:32:23.762805
8	add-public-to-buckets	fd670db39ed65f9d08b01db09d6202503ca2bab3	2025-07-21 09:32:23.76678
9	fix-search-function	3a0af29f42e35a4d101c259ed955b67e1bee6825	2025-07-21 09:32:23.770948
10	search-files-search-function	68dc14822daad0ffac3746a502234f486182ef6e	2025-07-21 09:32:23.775177
11	add-trigger-to-auto-update-updated_at-column	7425bdb14366d1739fa8a18c83100636d74dcaa2	2025-07-21 09:32:23.779969
12	add-automatic-avif-detection-flag	8e92e1266eb29518b6a4c5313ab8f29dd0d08df9	2025-07-21 09:32:23.790086
13	add-bucket-custom-limits	cce962054138135cd9a8c4bcd531598684b25e7d	2025-07-21 09:32:23.794633
14	use-bytes-for-max-size	941c41b346f9802b411f06f30e972ad4744dad27	2025-07-21 09:32:23.799495
15	add-can-insert-object-function	934146bc38ead475f4ef4b555c524ee5d66799e5	2025-07-21 09:32:23.818651
16	add-version	76debf38d3fd07dcfc747ca49096457d95b1221b	2025-07-21 09:32:23.822927
17	drop-owner-foreign-key	f1cbb288f1b7a4c1eb8c38504b80ae2a0153d101	2025-07-21 09:32:23.826684
18	add_owner_id_column_deprecate_owner	e7a511b379110b08e2f214be852c35414749fe66	2025-07-21 09:32:23.832217
19	alter-default-value-objects-id	02e5e22a78626187e00d173dc45f58fa66a4f043	2025-07-21 09:32:23.840091
20	list-objects-with-delimiter	cd694ae708e51ba82bf012bba00caf4f3b6393b7	2025-07-21 09:32:23.843806
21	s3-multipart-uploads	8c804d4a566c40cd1e4cc5b3725a664a9303657f	2025-07-21 09:32:23.850794
22	s3-multipart-uploads-big-ints	9737dc258d2397953c9953d9b86920b8be0cdb73	2025-07-21 09:32:23.862341
23	optimize-search-function	9d7e604cddc4b56a5422dc68c9313f4a1b6f132c	2025-07-21 09:32:23.872236
24	operation-function	8312e37c2bf9e76bbe841aa5fda889206d2bf8aa	2025-07-21 09:32:23.876774
25	custom-metadata	d974c6057c3db1c1f847afa0e291e6165693b990	2025-07-21 09:32:23.880464
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: optitab_db_user
--

COPY storage.objects (id, bucket_id, name, owner, created_at, updated_at, last_accessed_at, metadata, version, owner_id, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: optitab_db_user
--

COPY storage.s3_multipart_uploads (id, in_progress_size, upload_signature, bucket_id, key, version, owner_id, created_at, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: optitab_db_user
--

COPY storage.s3_multipart_uploads_parts (id, upload_id, size, part_number, bucket_id, key, etag, owner_id, version, created_at) FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: optitab_db_user
--

SELECT pg_catalog.setval('auth.refresh_tokens_id_seq', 1, false);


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 1, false);


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);


--
-- Name: ai_aiconversation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.ai_aiconversation_id_seq', 4, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 172, true);


--
-- Name: cours_cours_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.cours_cours_id_seq', 25, true);


--
-- Name: cours_coursimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.cours_coursimage_id_seq', 3, true);


--
-- Name: curriculum_exerciceimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.curriculum_exerciceimage_id_seq', 3, true);


--
-- Name: curriculum_matiere_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.curriculum_matiere_id_seq', 1, false);


--
-- Name: curriculum_matierecontexte_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.curriculum_matierecontexte_id_seq', 39, true);


--
-- Name: curriculum_notion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.curriculum_notion_id_seq', 47, true);


--
-- Name: curriculum_theme_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.curriculum_theme_id_seq', 36, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 222, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 42, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 100, true);


--
-- Name: django_rest_passwordreset_resetpasswordtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.django_rest_passwordreset_resetpasswordtoken_id_seq', 4, true);


--
-- Name: exercices_chapitre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.exercices_chapitre_id_seq', 46, true);


--
-- Name: exercices_exercice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.exercices_exercice_id_seq', 229, true);


--
-- Name: fiches_fichesynthese_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.fiches_fichesynthese_id_seq', 1, false);


--
-- Name: pays_niveaupays_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.pays_niveaupays_id_seq', 20, true);


--
-- Name: pays_pays_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.pays_pays_id_seq', 5, true);


--
-- Name: quiz_quiz_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.quiz_quiz_id_seq', 103, true);


--
-- Name: quiz_quizimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.quiz_quizimage_id_seq', 9, true);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.socialaccount_socialaccount_id_seq', 7, true);


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_id_seq', 1, false);


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.socialaccount_socialtoken_id_seq', 1, false);


--
-- Name: suivis_suiviexercice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.suivis_suiviexercice_id_seq', 317, true);


--
-- Name: suivis_suiviquiz_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.suivis_suiviquiz_id_seq', 176, true);


--
-- Name: synthesis_synthesissheet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.synthesis_synthesissheet_id_seq', 7, true);


--
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_customuser_groups_id_seq', 1, false);


--
-- Name: users_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_customuser_id_seq', 39, true);


--
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_customuser_user_permissions_id_seq', 1, false);


--
-- Name: users_parentchild_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_parentchild_id_seq', 4, true);


--
-- Name: users_userfavoritematiere_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_userfavoritematiere_id_seq', 29, true);


--
-- Name: users_usernotification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_usernotification_id_seq', 625, true);


--
-- Name: users_userselectedmatiere_id_seq; Type: SEQUENCE SET; Schema: public; Owner: optitab_db_user
--

SELECT pg_catalog.setval('public.users_userselectedmatiere_id_seq', 130, true);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: realtime; Owner: optitab_db_user
--

SELECT pg_catalog.setval('realtime.subscription_id_seq', 1, false);


--
-- Name: mfa_amr_claims amr_id_pk; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT amr_id_pk PRIMARY KEY (id);


--
-- Name: audit_log_entries audit_log_entries_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.audit_log_entries
    ADD CONSTRAINT audit_log_entries_pkey PRIMARY KEY (id);


--
-- Name: flow_state flow_state_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.flow_state
    ADD CONSTRAINT flow_state_pkey PRIMARY KEY (id);


--
-- Name: identities identities_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_pkey PRIMARY KEY (id);


--
-- Name: identities identities_provider_id_provider_unique; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_provider_id_provider_unique UNIQUE (provider_id, provider);


--
-- Name: instances instances_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.instances
    ADD CONSTRAINT instances_pkey PRIMARY KEY (id);


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_authentication_method_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_authentication_method_pkey UNIQUE (session_id, authentication_method);


--
-- Name: mfa_challenges mfa_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_pkey PRIMARY KEY (id);


--
-- Name: mfa_factors mfa_factors_last_challenged_at_key; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_last_challenged_at_key UNIQUE (last_challenged_at);


--
-- Name: mfa_factors mfa_factors_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_pkey PRIMARY KEY (id);


--
-- Name: one_time_tokens one_time_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_unique; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_unique UNIQUE (token);


--
-- Name: saml_providers saml_providers_entity_id_key; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_entity_id_key UNIQUE (entity_id);


--
-- Name: saml_providers saml_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_pkey PRIMARY KEY (id);


--
-- Name: saml_relay_states saml_relay_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sso_domains sso_domains_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_pkey PRIMARY KEY (id);


--
-- Name: sso_providers sso_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.sso_providers
    ADD CONSTRAINT sso_providers_pkey PRIMARY KEY (id);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress account_emailaddress_user_id_email_987c8728_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_email_987c8728_uniq UNIQUE (user_id, email);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: ai_aiconversation ai_aiconversation_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.ai_aiconversation
    ADD CONSTRAINT ai_aiconversation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: cours_cours cours_cours_chapitre_id_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.cours_cours
    ADD CONSTRAINT cours_cours_chapitre_id_key UNIQUE (chapitre_id);


--
-- Name: cours_cours cours_cours_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.cours_cours
    ADD CONSTRAINT cours_cours_pkey PRIMARY KEY (id);


--
-- Name: cours_coursimage cours_coursimage_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.cours_coursimage
    ADD CONSTRAINT cours_coursimage_pkey PRIMARY KEY (id);


--
-- Name: curriculum_exerciceimage curriculum_exerciceimage_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_exerciceimage
    ADD CONSTRAINT curriculum_exerciceimage_pkey PRIMARY KEY (id);


--
-- Name: curriculum_matiere curriculum_matiere_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_matiere
    ADD CONSTRAINT curriculum_matiere_pkey PRIMARY KEY (id);


--
-- Name: curriculum_matierecontexte curriculum_matierecontexte_matiere_id_niveau_id_408a3fd5_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_matierecontexte
    ADD CONSTRAINT curriculum_matierecontexte_matiere_id_niveau_id_408a3fd5_uniq UNIQUE (matiere_id, niveau_id);


--
-- Name: curriculum_matierecontexte curriculum_matierecontexte_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_matierecontexte
    ADD CONSTRAINT curriculum_matierecontexte_pkey PRIMARY KEY (id);


--
-- Name: curriculum_notion curriculum_notion_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_notion
    ADD CONSTRAINT curriculum_notion_pkey PRIMARY KEY (id);


--
-- Name: curriculum_notion curriculum_notion_theme_id_titre_991a534c_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_notion
    ADD CONSTRAINT curriculum_notion_theme_id_titre_991a534c_uniq UNIQUE (theme_id, titre);


--
-- Name: curriculum_theme curriculum_theme_contexte_id_titre_fad8ed15_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_theme
    ADD CONSTRAINT curriculum_theme_contexte_id_titre_fad8ed15_uniq UNIQUE (contexte_id, titre);


--
-- Name: curriculum_theme curriculum_theme_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_theme
    ADD CONSTRAINT curriculum_theme_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_rest_passwordreset_resetpasswordtoken django_rest_passwordreset_resetpasswordtoken_key_f1b65873_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_rest_passwordreset_resetpasswordtoken
    ADD CONSTRAINT django_rest_passwordreset_resetpasswordtoken_key_f1b65873_uniq UNIQUE (key);


--
-- Name: django_rest_passwordreset_resetpasswordtoken django_rest_passwordreset_resetpasswordtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_rest_passwordreset_resetpasswordtoken
    ADD CONSTRAINT django_rest_passwordreset_resetpasswordtoken_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: curriculum_chapitre exercices_chapitre_notion_id_titre_5fd4d959_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_chapitre
    ADD CONSTRAINT exercices_chapitre_notion_id_titre_5fd4d959_uniq UNIQUE (notion_id, titre);


--
-- Name: curriculum_chapitre exercices_chapitre_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_chapitre
    ADD CONSTRAINT exercices_chapitre_pkey PRIMARY KEY (id);


--
-- Name: curriculum_exercice exercices_exercice_chapitre_id_titre_7a4c4119_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_exercice
    ADD CONSTRAINT exercices_exercice_chapitre_id_titre_7a4c4119_uniq UNIQUE (chapitre_id, titre);


--
-- Name: curriculum_exercice exercices_exercice_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_exercice
    ADD CONSTRAINT exercices_exercice_pkey PRIMARY KEY (id);


--
-- Name: curriculum_notion exercices_notion_theme_id_titre_ae10a7ee_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_notion
    ADD CONSTRAINT exercices_notion_theme_id_titre_ae10a7ee_uniq UNIQUE (theme_id, titre);


--
-- Name: fiches_fichesynthese fiches_fichesynthese_notion_id_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.fiches_fichesynthese
    ADD CONSTRAINT fiches_fichesynthese_notion_id_key UNIQUE (notion_id);


--
-- Name: fiches_fichesynthese fiches_fichesynthese_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.fiches_fichesynthese
    ADD CONSTRAINT fiches_fichesynthese_pkey PRIMARY KEY (id);


--
-- Name: pays_niveau pays_niveaupays_pays_id_nom_96a39e18_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.pays_niveau
    ADD CONSTRAINT pays_niveaupays_pays_id_nom_96a39e18_uniq UNIQUE (pays_id, nom);


--
-- Name: pays_niveau pays_niveaupays_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.pays_niveau
    ADD CONSTRAINT pays_niveaupays_pkey PRIMARY KEY (id);


--
-- Name: pays_pays pays_pays_code_iso_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.pays_pays
    ADD CONSTRAINT pays_pays_code_iso_key UNIQUE (code_iso);


--
-- Name: pays_pays pays_pays_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.pays_pays
    ADD CONSTRAINT pays_pays_pkey PRIMARY KEY (id);


--
-- Name: quiz_quiz quiz_quiz_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.quiz_quiz
    ADD CONSTRAINT quiz_quiz_pkey PRIMARY KEY (id);


--
-- Name: quiz_quizimage quiz_quizimage_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.quiz_quizimage
    ADD CONSTRAINT quiz_quizimage_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: suivis_suiviexercice suivis_suiviexercice_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviexercice
    ADD CONSTRAINT suivis_suiviexercice_pkey PRIMARY KEY (id);


--
-- Name: suivis_suiviexercice suivis_suiviexercice_user_id_exercice_id_3d6b00f5_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviexercice
    ADD CONSTRAINT suivis_suiviexercice_user_id_exercice_id_3d6b00f5_uniq UNIQUE (user_id, exercice_id);


--
-- Name: suivis_suiviquiz suivis_suiviquiz_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviquiz
    ADD CONSTRAINT suivis_suiviquiz_pkey PRIMARY KEY (id);


--
-- Name: suivis_suiviquiz suivis_suiviquiz_user_id_quiz_id_tentative_numero_7d60d0bf_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviquiz
    ADD CONSTRAINT suivis_suiviquiz_user_id_quiz_id_tentative_numero_7d60d0bf_uniq UNIQUE (user_id, quiz_id, tentative_numero);


--
-- Name: synthesis_synthesissheet synthesis_synthesissheet_notion_id_titre_a67aabb0_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.synthesis_synthesissheet
    ADD CONSTRAINT synthesis_synthesissheet_notion_id_titre_a67aabb0_uniq UNIQUE (notion_id, titre);


--
-- Name: synthesis_synthesissheet synthesis_synthesissheet_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.synthesis_synthesissheet
    ADD CONSTRAINT synthesis_synthesissheet_pkey PRIMARY KEY (id);


--
-- Name: users_customuser users_customuser_email_key; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_email_key UNIQUE (email);


--
-- Name: users_customuser_groups users_customuser_groups_customuser_id_group_id_76b619e3_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_customuser_id_group_id_76b619e3_uniq UNIQUE (customuser_id, group_id);


--
-- Name: users_customuser_groups users_customuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_pkey PRIMARY KEY (id);


--
-- Name: users_customuser users_customuser_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_pkey PRIMARY KEY (id);


--
-- Name: users_customuser_user_permissions users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq UNIQUE (customuser_id, permission_id);


--
-- Name: users_customuser_user_permissions users_customuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_parentchild users_parentchild_parent_id_child_id_2996bbbf_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_parentchild
    ADD CONSTRAINT users_parentchild_parent_id_child_id_2996bbbf_uniq UNIQUE (parent_id, child_id);


--
-- Name: users_parentchild users_parentchild_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_parentchild
    ADD CONSTRAINT users_parentchild_pkey PRIMARY KEY (id);


--
-- Name: users_userfavoritematiere users_userfavoritematiere_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userfavoritematiere
    ADD CONSTRAINT users_userfavoritematiere_pkey PRIMARY KEY (id);


--
-- Name: users_userfavoritematiere users_userfavoritematiere_user_id_matiere_id_59156a14_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userfavoritematiere
    ADD CONSTRAINT users_userfavoritematiere_user_id_matiere_id_59156a14_uniq UNIQUE (user_id, matiere_id);


--
-- Name: users_usernotification users_usernotification_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_usernotification
    ADD CONSTRAINT users_usernotification_pkey PRIMARY KEY (id);


--
-- Name: users_userselectedmatiere users_userselectedmatiere_pkey; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userselectedmatiere
    ADD CONSTRAINT users_userselectedmatiere_pkey PRIMARY KEY (id);


--
-- Name: users_userselectedmatiere users_userselectedmatiere_user_id_matiere_id_4951f4f7_uniq; Type: CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userselectedmatiere
    ADD CONSTRAINT users_userselectedmatiere_user_id_matiere_id_4951f4f7_uniq UNIQUE (user_id, matiere_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: realtime; Owner: optitab_db_user
--

ALTER TABLE ONLY realtime.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id, inserted_at);


--
-- Name: subscription pk_subscription; Type: CONSTRAINT; Schema: realtime; Owner: optitab_db_user
--

ALTER TABLE ONLY realtime.subscription
    ADD CONSTRAINT pk_subscription PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: realtime; Owner: optitab_db_user
--

ALTER TABLE ONLY realtime.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: buckets buckets_pkey; Type: CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.buckets
    ADD CONSTRAINT buckets_pkey PRIMARY KEY (id);


--
-- Name: migrations migrations_name_key; Type: CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_name_key UNIQUE (name);


--
-- Name: migrations migrations_pkey; Type: CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_pkey; Type: CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_pkey; Type: CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_pkey PRIMARY KEY (id);


--
-- Name: audit_logs_instance_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX audit_logs_instance_id_idx ON auth.audit_log_entries USING btree (instance_id);


--
-- Name: confirmation_token_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX confirmation_token_idx ON auth.users USING btree (confirmation_token) WHERE ((confirmation_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: email_change_token_current_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX email_change_token_current_idx ON auth.users USING btree (email_change_token_current) WHERE ((email_change_token_current)::text !~ '^[0-9 ]*$'::text);


--
-- Name: email_change_token_new_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX email_change_token_new_idx ON auth.users USING btree (email_change_token_new) WHERE ((email_change_token_new)::text !~ '^[0-9 ]*$'::text);


--
-- Name: factor_id_created_at_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX factor_id_created_at_idx ON auth.mfa_factors USING btree (user_id, created_at);


--
-- Name: flow_state_created_at_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX flow_state_created_at_idx ON auth.flow_state USING btree (created_at DESC);


--
-- Name: identities_email_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX identities_email_idx ON auth.identities USING btree (email text_pattern_ops);


--
-- Name: INDEX identities_email_idx; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON INDEX auth.identities_email_idx IS 'Auth: Ensures indexed queries on the email column';


--
-- Name: identities_user_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX identities_user_id_idx ON auth.identities USING btree (user_id);


--
-- Name: idx_auth_code; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX idx_auth_code ON auth.flow_state USING btree (auth_code);


--
-- Name: idx_user_id_auth_method; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX idx_user_id_auth_method ON auth.flow_state USING btree (user_id, authentication_method);


--
-- Name: mfa_challenge_created_at_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX mfa_challenge_created_at_idx ON auth.mfa_challenges USING btree (created_at DESC);


--
-- Name: mfa_factors_user_friendly_name_unique; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX mfa_factors_user_friendly_name_unique ON auth.mfa_factors USING btree (friendly_name, user_id) WHERE (TRIM(BOTH FROM friendly_name) <> ''::text);


--
-- Name: mfa_factors_user_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX mfa_factors_user_id_idx ON auth.mfa_factors USING btree (user_id);


--
-- Name: one_time_tokens_relates_to_hash_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX one_time_tokens_relates_to_hash_idx ON auth.one_time_tokens USING hash (relates_to);


--
-- Name: one_time_tokens_token_hash_hash_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX one_time_tokens_token_hash_hash_idx ON auth.one_time_tokens USING hash (token_hash);


--
-- Name: one_time_tokens_user_id_token_type_key; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX one_time_tokens_user_id_token_type_key ON auth.one_time_tokens USING btree (user_id, token_type);


--
-- Name: reauthentication_token_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX reauthentication_token_idx ON auth.users USING btree (reauthentication_token) WHERE ((reauthentication_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: recovery_token_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX recovery_token_idx ON auth.users USING btree (recovery_token) WHERE ((recovery_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: refresh_tokens_instance_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX refresh_tokens_instance_id_idx ON auth.refresh_tokens USING btree (instance_id);


--
-- Name: refresh_tokens_instance_id_user_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX refresh_tokens_instance_id_user_id_idx ON auth.refresh_tokens USING btree (instance_id, user_id);


--
-- Name: refresh_tokens_parent_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX refresh_tokens_parent_idx ON auth.refresh_tokens USING btree (parent);


--
-- Name: refresh_tokens_session_id_revoked_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX refresh_tokens_session_id_revoked_idx ON auth.refresh_tokens USING btree (session_id, revoked);


--
-- Name: refresh_tokens_updated_at_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX refresh_tokens_updated_at_idx ON auth.refresh_tokens USING btree (updated_at DESC);


--
-- Name: saml_providers_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX saml_providers_sso_provider_id_idx ON auth.saml_providers USING btree (sso_provider_id);


--
-- Name: saml_relay_states_created_at_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX saml_relay_states_created_at_idx ON auth.saml_relay_states USING btree (created_at DESC);


--
-- Name: saml_relay_states_for_email_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX saml_relay_states_for_email_idx ON auth.saml_relay_states USING btree (for_email);


--
-- Name: saml_relay_states_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX saml_relay_states_sso_provider_id_idx ON auth.saml_relay_states USING btree (sso_provider_id);


--
-- Name: sessions_not_after_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX sessions_not_after_idx ON auth.sessions USING btree (not_after DESC);


--
-- Name: sessions_user_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX sessions_user_id_idx ON auth.sessions USING btree (user_id);


--
-- Name: sso_domains_domain_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX sso_domains_domain_idx ON auth.sso_domains USING btree (lower(domain));


--
-- Name: sso_domains_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX sso_domains_sso_provider_id_idx ON auth.sso_domains USING btree (sso_provider_id);


--
-- Name: sso_providers_resource_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX sso_providers_resource_id_idx ON auth.sso_providers USING btree (lower(resource_id));


--
-- Name: unique_phone_factor_per_user; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX unique_phone_factor_per_user ON auth.mfa_factors USING btree (user_id, phone);


--
-- Name: user_id_created_at_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX user_id_created_at_idx ON auth.sessions USING btree (user_id, created_at);


--
-- Name: users_email_partial_key; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE UNIQUE INDEX users_email_partial_key ON auth.users USING btree (email) WHERE (is_sso_user = false);


--
-- Name: INDEX users_email_partial_key; Type: COMMENT; Schema: auth; Owner: optitab_db_user
--

COMMENT ON INDEX auth.users_email_partial_key IS 'Auth: A partial unique index that applies only when is_sso_user is false';


--
-- Name: users_instance_id_email_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX users_instance_id_email_idx ON auth.users USING btree (instance_id, lower((email)::text));


--
-- Name: users_instance_id_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX users_instance_id_idx ON auth.users USING btree (instance_id);


--
-- Name: users_is_anonymous_idx; Type: INDEX; Schema: auth; Owner: optitab_db_user
--

CREATE INDEX users_is_anonymous_idx ON auth.users USING btree (is_anonymous);


--
-- Name: account_emailaddress_email_03be32b2; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX account_emailaddress_email_03be32b2 ON public.account_emailaddress USING btree (email);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: ai_aiconver_context_087723_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX ai_aiconver_context_087723_idx ON public.ai_aiconversation USING btree (contexte_chapitre_id);


--
-- Name: ai_aiconver_context_f0ca99_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX ai_aiconver_context_f0ca99_idx ON public.ai_aiconversation USING btree (contexte_matiere_id);


--
-- Name: ai_aiconver_user_id_317f36_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX ai_aiconver_user_id_317f36_idx ON public.ai_aiconversation USING btree (user_id, created_at DESC);


--
-- Name: ai_aiconversation_contexte_chapitre_id_f6422edc; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX ai_aiconversation_contexte_chapitre_id_f6422edc ON public.ai_aiconversation USING btree (contexte_chapitre_id);


--
-- Name: ai_aiconversation_contexte_matiere_id_f03bb831; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX ai_aiconversation_contexte_matiere_id_f03bb831 ON public.ai_aiconversation USING btree (contexte_matiere_id);


--
-- Name: ai_aiconversation_user_id_61da3c20; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX ai_aiconversation_user_id_61da3c20 ON public.ai_aiconversation USING btree (user_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: cours_cours_cours_i_f3f936_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX cours_cours_cours_i_f3f936_idx ON public.cours_coursimage USING btree (cours_id, "position");


--
-- Name: cours_coursimage_cours_id_09b57deb; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX cours_coursimage_cours_id_09b57deb ON public.cours_coursimage USING btree (cours_id);


--
-- Name: curriculum__exercic_178924_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum__exercic_178924_idx ON public.curriculum_exerciceimage USING btree (exercice_id, "position");


--
-- Name: curriculum_exerciceimage_exercice_id_d0e4326b; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum_exerciceimage_exercice_id_d0e4326b ON public.curriculum_exerciceimage USING btree (exercice_id);


--
-- Name: curriculum_matierecontexte_matiere_id_85edd62a; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum_matierecontexte_matiere_id_85edd62a ON public.curriculum_matierecontexte USING btree (matiere_id);


--
-- Name: curriculum_matierecontexte_niveau_id_d1f17f35; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum_matierecontexte_niveau_id_d1f17f35 ON public.curriculum_matierecontexte USING btree (niveau_id);


--
-- Name: curriculum_notion_theme_id_a68243eb; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum_notion_theme_id_a68243eb ON public.curriculum_notion USING btree (theme_id);


--
-- Name: curriculum_theme_contexte_id_34187d46; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum_theme_contexte_id_34187d46 ON public.curriculum_theme USING btree (contexte_id);


--
-- Name: curriculum_theme_matiere_id_f0da1cc1; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX curriculum_theme_matiere_id_f0da1cc1 ON public.curriculum_theme USING btree (matiere_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_rest_passwordreset_resetpasswordtoken_key_f1b65873_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX django_rest_passwordreset_resetpasswordtoken_key_f1b65873_like ON public.django_rest_passwordreset_resetpasswordtoken USING btree (key varchar_pattern_ops);


--
-- Name: django_rest_passwordreset_resetpasswordtoken_user_id_e8015b11; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX django_rest_passwordreset_resetpasswordtoken_user_id_e8015b11 ON public.django_rest_passwordreset_resetpasswordtoken USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: exercices_chapitre_notion_id_2d48f86f; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX exercices_chapitre_notion_id_2d48f86f ON public.curriculum_chapitre USING btree (notion_id);


--
-- Name: exercices_exercice_chapitre_id_a145be17; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX exercices_exercice_chapitre_id_a145be17 ON public.curriculum_exercice USING btree (chapitre_id);


--
-- Name: exercices_notion_theme_id_046b73e8; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX exercices_notion_theme_id_046b73e8 ON public.curriculum_notion USING btree (theme_id);


--
-- Name: exercices_theme_matiere_id_5d95b01d; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX exercices_theme_matiere_id_5d95b01d ON public.curriculum_theme USING btree (matiere_id);


--
-- Name: pays_niveaupays_pays_id_8356e942; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX pays_niveaupays_pays_id_8356e942 ON public.pays_niveau USING btree (pays_id);


--
-- Name: pays_pays_code_iso_ff5ae090_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX pays_pays_code_iso_ff5ae090_like ON public.pays_pays USING btree (code_iso varchar_pattern_ops);


--
-- Name: quiz_quiz_chapitre_id_9bba2ba7; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX quiz_quiz_chapitre_id_9bba2ba7 ON public.quiz_quiz USING btree (chapitre_id);


--
-- Name: quiz_quizim_quiz_id_5d326a_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX quiz_quizim_quiz_id_5d326a_idx ON public.quiz_quizimage USING btree (quiz_id, "position");


--
-- Name: quiz_quizimage_quiz_id_20f3c781; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX quiz_quizimage_quiz_id_20f3c781 ON public.quiz_quizimage USING btree (quiz_id);


--
-- Name: socialaccount_socialaccount_user_id_8146e70c; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON public.socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialtoken_account_id_951f210e; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON public.socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_app_id_636a42d7; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON public.socialaccount_socialtoken USING btree (app_id);


--
-- Name: suivis_suiviexercice_exercice_id_ae12824e; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX suivis_suiviexercice_exercice_id_ae12824e ON public.suivis_suiviexercice USING btree (exercice_id);


--
-- Name: suivis_suiviexercice_user_id_dad7aa63; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX suivis_suiviexercice_user_id_dad7aa63 ON public.suivis_suiviexercice USING btree (user_id);


--
-- Name: suivis_suiviquiz_quiz_id_ea79731a; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX suivis_suiviquiz_quiz_id_ea79731a ON public.suivis_suiviquiz USING btree (quiz_id);


--
-- Name: suivis_suiviquiz_user_id_9b984811; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX suivis_suiviquiz_user_id_9b984811 ON public.suivis_suiviquiz USING btree (user_id);


--
-- Name: synthesis_synthesissheet_notion_id_a70d09bd; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX synthesis_synthesissheet_notion_id_a70d09bd ON public.synthesis_synthesissheet USING btree (notion_id);


--
-- Name: unique_primary_email; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE UNIQUE INDEX unique_primary_email ON public.account_emailaddress USING btree (user_id, "primary") WHERE "primary";


--
-- Name: unique_verified_email; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE UNIQUE INDEX unique_verified_email ON public.account_emailaddress USING btree (email) WHERE verified;


--
-- Name: users_customuser_email_6445acef_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_email_6445acef_like ON public.users_customuser USING btree (email varchar_pattern_ops);


--
-- Name: users_customuser_groups_customuser_id_958147bf; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_groups_customuser_id_958147bf ON public.users_customuser_groups USING btree (customuser_id);


--
-- Name: users_customuser_groups_group_id_01390b14; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_groups_group_id_01390b14 ON public.users_customuser_groups USING btree (group_id);


--
-- Name: users_customuser_niveau_pays_id_35e090f6; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_niveau_pays_id_35e090f6 ON public.users_customuser USING btree (niveau_pays_id);


--
-- Name: users_customuser_pays_id_90d8796e; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_pays_id_90d8796e ON public.users_customuser USING btree (pays_id);


--
-- Name: users_customuser_role_1fa6b9f9; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_role_1fa6b9f9 ON public.users_customuser USING btree (role);


--
-- Name: users_customuser_role_1fa6b9f9_like; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_role_1fa6b9f9_like ON public.users_customuser USING btree (role varchar_pattern_ops);


--
-- Name: users_customuser_user_permissions_customuser_id_5771478b; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_user_permissions_customuser_id_5771478b ON public.users_customuser_user_permissions USING btree (customuser_id);


--
-- Name: users_customuser_user_permissions_permission_id_baaa2f74; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_customuser_user_permissions_permission_id_baaa2f74 ON public.users_customuser_user_permissions USING btree (permission_id);


--
-- Name: users_paren_parent__e314ac_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_paren_parent__e314ac_idx ON public.users_parentchild USING btree (parent_id, child_id);


--
-- Name: users_parentchild_child_id_d9b65117; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_parentchild_child_id_d9b65117 ON public.users_parentchild USING btree (child_id);


--
-- Name: users_parentchild_parent_id_1ff9b6fe; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_parentchild_parent_id_1ff9b6fe ON public.users_parentchild USING btree (parent_id);


--
-- Name: users_userfavoritematiere_matiere_id_f02464ac; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_userfavoritematiere_matiere_id_f02464ac ON public.users_userfavoritematiere USING btree (matiere_id);


--
-- Name: users_userfavoritematiere_user_id_b9676792; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_userfavoritematiere_user_id_b9676792 ON public.users_userfavoritematiere USING btree (user_id);


--
-- Name: users_usern_user_id_55f2d2_idx; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_usern_user_id_55f2d2_idx ON public.users_usernotification USING btree (user_id, read, created_at DESC);


--
-- Name: users_usernotification_created_at_05da1bf7; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_usernotification_created_at_05da1bf7 ON public.users_usernotification USING btree (created_at);


--
-- Name: users_usernotification_read_3e01699c; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_usernotification_read_3e01699c ON public.users_usernotification USING btree (read);


--
-- Name: users_usernotification_user_id_4cef5e00; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_usernotification_user_id_4cef5e00 ON public.users_usernotification USING btree (user_id);


--
-- Name: users_userselectedmatiere_matiere_id_0eac9021; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_userselectedmatiere_matiere_id_0eac9021 ON public.users_userselectedmatiere USING btree (matiere_id);


--
-- Name: users_userselectedmatiere_user_id_67e6b1d0; Type: INDEX; Schema: public; Owner: optitab_db_user
--

CREATE INDEX users_userselectedmatiere_user_id_67e6b1d0 ON public.users_userselectedmatiere USING btree (user_id);


--
-- Name: ix_realtime_subscription_entity; Type: INDEX; Schema: realtime; Owner: optitab_db_user
--

CREATE INDEX ix_realtime_subscription_entity ON realtime.subscription USING btree (entity);


--
-- Name: subscription_subscription_id_entity_filters_key; Type: INDEX; Schema: realtime; Owner: optitab_db_user
--

CREATE UNIQUE INDEX subscription_subscription_id_entity_filters_key ON realtime.subscription USING btree (subscription_id, entity, filters);


--
-- Name: bname; Type: INDEX; Schema: storage; Owner: optitab_db_user
--

CREATE UNIQUE INDEX bname ON storage.buckets USING btree (name);


--
-- Name: bucketid_objname; Type: INDEX; Schema: storage; Owner: optitab_db_user
--

CREATE UNIQUE INDEX bucketid_objname ON storage.objects USING btree (bucket_id, name);


--
-- Name: idx_multipart_uploads_list; Type: INDEX; Schema: storage; Owner: optitab_db_user
--

CREATE INDEX idx_multipart_uploads_list ON storage.s3_multipart_uploads USING btree (bucket_id, key, created_at);


--
-- Name: idx_objects_bucket_id_name; Type: INDEX; Schema: storage; Owner: optitab_db_user
--

CREATE INDEX idx_objects_bucket_id_name ON storage.objects USING btree (bucket_id, name COLLATE "C");


--
-- Name: name_prefix_search; Type: INDEX; Schema: storage; Owner: optitab_db_user
--

CREATE INDEX name_prefix_search ON storage.objects USING btree (name text_pattern_ops);


--
-- Name: subscription tr_check_filters; Type: TRIGGER; Schema: realtime; Owner: optitab_db_user
--

CREATE TRIGGER tr_check_filters BEFORE INSERT OR UPDATE ON realtime.subscription FOR EACH ROW EXECUTE FUNCTION realtime.subscription_check_filters();


--
-- Name: objects update_objects_updated_at; Type: TRIGGER; Schema: storage; Owner: optitab_db_user
--

CREATE TRIGGER update_objects_updated_at BEFORE UPDATE ON storage.objects FOR EACH ROW EXECUTE FUNCTION storage.update_updated_at_column();


--
-- Name: identities identities_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: mfa_challenges mfa_challenges_auth_factor_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_auth_factor_id_fkey FOREIGN KEY (factor_id) REFERENCES auth.mfa_factors(id) ON DELETE CASCADE;


--
-- Name: mfa_factors mfa_factors_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: one_time_tokens one_time_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: refresh_tokens refresh_tokens_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: saml_providers saml_providers_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_flow_state_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_flow_state_id_fkey FOREIGN KEY (flow_state_id) REFERENCES auth.flow_state(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: sso_domains sso_domains_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ai_aiconversation ai_aiconversation_contexte_chapitre_id_f6422edc_fk_curriculu; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.ai_aiconversation
    ADD CONSTRAINT ai_aiconversation_contexte_chapitre_id_f6422edc_fk_curriculu FOREIGN KEY (contexte_chapitre_id) REFERENCES public.curriculum_chapitre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ai_aiconversation ai_aiconversation_contexte_matiere_id_f03bb831_fk_curriculu; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.ai_aiconversation
    ADD CONSTRAINT ai_aiconversation_contexte_matiere_id_f03bb831_fk_curriculu FOREIGN KEY (contexte_matiere_id) REFERENCES public.curriculum_matierecontexte(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ai_aiconversation ai_aiconversation_user_id_61da3c20_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.ai_aiconversation
    ADD CONSTRAINT ai_aiconversation_user_id_61da3c20_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cours_cours cours_cours_chapitre_id_4d6aebcc_fk_exercices_chapitre_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.cours_cours
    ADD CONSTRAINT cours_cours_chapitre_id_4d6aebcc_fk_exercices_chapitre_id FOREIGN KEY (chapitre_id) REFERENCES public.curriculum_chapitre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cours_coursimage cours_coursimage_cours_id_09b57deb_fk_cours_cours_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.cours_coursimage
    ADD CONSTRAINT cours_coursimage_cours_id_09b57deb_fk_cours_cours_id FOREIGN KEY (cours_id) REFERENCES public.cours_cours(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_exerciceimage curriculum_exercicei_exercice_id_d0e4326b_fk_curriculu; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_exerciceimage
    ADD CONSTRAINT curriculum_exercicei_exercice_id_d0e4326b_fk_curriculu FOREIGN KEY (exercice_id) REFERENCES public.curriculum_exercice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_matierecontexte curriculum_matiereco_matiere_id_85edd62a_fk_curriculu; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_matierecontexte
    ADD CONSTRAINT curriculum_matiereco_matiere_id_85edd62a_fk_curriculu FOREIGN KEY (matiere_id) REFERENCES public.curriculum_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_matierecontexte curriculum_matierecontexte_niveau_id_d1f17f35_fk_pays_niveau_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_matierecontexte
    ADD CONSTRAINT curriculum_matierecontexte_niveau_id_d1f17f35_fk_pays_niveau_id FOREIGN KEY (niveau_id) REFERENCES public.pays_niveau(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_notion curriculum_notion_theme_id_a68243eb_fk_curriculum_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_notion
    ADD CONSTRAINT curriculum_notion_theme_id_a68243eb_fk_curriculum_theme_id FOREIGN KEY (theme_id) REFERENCES public.curriculum_theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_theme curriculum_theme_contexte_id_34187d46_fk_curriculu; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_theme
    ADD CONSTRAINT curriculum_theme_contexte_id_34187d46_fk_curriculu FOREIGN KEY (contexte_id) REFERENCES public.curriculum_matierecontexte(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_theme curriculum_theme_matiere_id_f0da1cc1_fk_curriculum_matiere_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_theme
    ADD CONSTRAINT curriculum_theme_matiere_id_f0da1cc1_fk_curriculum_matiere_id FOREIGN KEY (matiere_id) REFERENCES public.curriculum_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_rest_passwordreset_resetpasswordtoken django_rest_password_user_id_e8015b11_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.django_rest_passwordreset_resetpasswordtoken
    ADD CONSTRAINT django_rest_password_user_id_e8015b11_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_chapitre exercices_chapitre_notion_id_2d48f86f_fk_exercices_notion_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_chapitre
    ADD CONSTRAINT exercices_chapitre_notion_id_2d48f86f_fk_exercices_notion_id FOREIGN KEY (notion_id) REFERENCES public.curriculum_notion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_exercice exercices_exercice_chapitre_id_a145be17_fk_exercices; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_exercice
    ADD CONSTRAINT exercices_exercice_chapitre_id_a145be17_fk_exercices FOREIGN KEY (chapitre_id) REFERENCES public.curriculum_chapitre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_notion exercices_notion_theme_id_046b73e8_fk_exercices_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_notion
    ADD CONSTRAINT exercices_notion_theme_id_046b73e8_fk_exercices_theme_id FOREIGN KEY (theme_id) REFERENCES public.curriculum_theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: curriculum_theme exercices_theme_matiere_id_5d95b01d_fk_exercices_matiere_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.curriculum_theme
    ADD CONSTRAINT exercices_theme_matiere_id_5d95b01d_fk_exercices_matiere_id FOREIGN KEY (matiere_id) REFERENCES public.curriculum_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fiches_fichesynthese fiches_fichesynthese_notion_id_90be4ff5_fk_exercices_notion_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.fiches_fichesynthese
    ADD CONSTRAINT fiches_fichesynthese_notion_id_90be4ff5_fk_exercices_notion_id FOREIGN KEY (notion_id) REFERENCES public.curriculum_notion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pays_niveau pays_niveaupays_pays_id_8356e942_fk_pays_pays_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.pays_niveau
    ADD CONSTRAINT pays_niveaupays_pays_id_8356e942_fk_pays_pays_id FOREIGN KEY (pays_id) REFERENCES public.pays_pays(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quiz_quiz quiz_quiz_chapitre_id_9bba2ba7_fk_exercices_chapitre_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.quiz_quiz
    ADD CONSTRAINT quiz_quiz_chapitre_id_9bba2ba7_fk_exercices_chapitre_id FOREIGN KEY (chapitre_id) REFERENCES public.curriculum_chapitre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quiz_quizimage quiz_quizimage_quiz_id_20f3c781_fk_quiz_quiz_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.quiz_quizimage
    ADD CONSTRAINT quiz_quizimage_quiz_id_20f3c781_fk_quiz_quiz_id FOREIGN KEY (quiz_id) REFERENCES public.quiz_quiz(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_social_user_id_8146e70c_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_social_user_id_8146e70c_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: suivis_suiviexercice suivis_suiviexercice_exercice_id_ae12824e_fk_exercices; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviexercice
    ADD CONSTRAINT suivis_suiviexercice_exercice_id_ae12824e_fk_exercices FOREIGN KEY (exercice_id) REFERENCES public.curriculum_exercice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: suivis_suiviexercice suivis_suiviexercice_user_id_dad7aa63_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviexercice
    ADD CONSTRAINT suivis_suiviexercice_user_id_dad7aa63_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: suivis_suiviquiz suivis_suiviquiz_quiz_id_ea79731a_fk_quiz_quiz_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviquiz
    ADD CONSTRAINT suivis_suiviquiz_quiz_id_ea79731a_fk_quiz_quiz_id FOREIGN KEY (quiz_id) REFERENCES public.quiz_quiz(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: suivis_suiviquiz suivis_suiviquiz_user_id_9b984811_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.suivis_suiviquiz
    ADD CONSTRAINT suivis_suiviquiz_user_id_9b984811_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: synthesis_synthesissheet synthesis_synthesiss_notion_id_a70d09bd_fk_curriculu; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.synthesis_synthesissheet
    ADD CONSTRAINT synthesis_synthesiss_notion_id_a70d09bd_fk_curriculu FOREIGN KEY (notion_id) REFERENCES public.curriculum_notion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_groups users_customuser_gro_customuser_id_958147bf_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_gro_customuser_id_958147bf_fk_users_cus FOREIGN KEY (customuser_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_groups users_customuser_groups_group_id_01390b14_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_group_id_01390b14_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser users_customuser_niveau_pays_id_35e090f6_fk_pays_niveau_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_niveau_pays_id_35e090f6_fk_pays_niveau_id FOREIGN KEY (niveau_pays_id) REFERENCES public.pays_niveau(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser users_customuser_pays_id_90d8796e_fk_pays_pays_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_pays_id_90d8796e_fk_pays_pays_id FOREIGN KEY (pays_id) REFERENCES public.pays_pays(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_user_permissions users_customuser_use_customuser_id_5771478b_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_use_customuser_id_5771478b_fk_users_cus FOREIGN KEY (customuser_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_user_permissions users_customuser_use_permission_id_baaa2f74_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_use_permission_id_baaa2f74_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_parentchild users_parentchild_child_id_d9b65117_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_parentchild
    ADD CONSTRAINT users_parentchild_child_id_d9b65117_fk_users_customuser_id FOREIGN KEY (child_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_parentchild users_parentchild_parent_id_1ff9b6fe_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_parentchild
    ADD CONSTRAINT users_parentchild_parent_id_1ff9b6fe_fk_users_customuser_id FOREIGN KEY (parent_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userfavoritematiere users_userfavoritema_matiere_id_f02464ac_fk_exercices; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userfavoritematiere
    ADD CONSTRAINT users_userfavoritema_matiere_id_f02464ac_fk_exercices FOREIGN KEY (matiere_id) REFERENCES public.curriculum_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userfavoritematiere users_userfavoritema_user_id_b9676792_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userfavoritematiere
    ADD CONSTRAINT users_userfavoritema_user_id_b9676792_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_usernotification users_usernotification_user_id_4cef5e00_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_usernotification
    ADD CONSTRAINT users_usernotification_user_id_4cef5e00_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userselectedmatiere users_userselectedma_matiere_id_0eac9021_fk_exercices; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userselectedmatiere
    ADD CONSTRAINT users_userselectedma_matiere_id_0eac9021_fk_exercices FOREIGN KEY (matiere_id) REFERENCES public.curriculum_matiere(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userselectedmatiere users_userselectedma_user_id_67e6b1d0_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: optitab_db_user
--

ALTER TABLE ONLY public.users_userselectedmatiere
    ADD CONSTRAINT users_userselectedma_user_id_67e6b1d0_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: objects objects_bucketId_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT "objects_bucketId_fkey" FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_upload_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_upload_id_fkey FOREIGN KEY (upload_id) REFERENCES storage.s3_multipart_uploads(id) ON DELETE CASCADE;


--
-- Name: audit_log_entries; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.audit_log_entries ENABLE ROW LEVEL SECURITY;

--
-- Name: flow_state; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.flow_state ENABLE ROW LEVEL SECURITY;

--
-- Name: identities; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.identities ENABLE ROW LEVEL SECURITY;

--
-- Name: instances; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.instances ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_amr_claims; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.mfa_amr_claims ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_challenges; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.mfa_challenges ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_factors; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.mfa_factors ENABLE ROW LEVEL SECURITY;

--
-- Name: one_time_tokens; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.one_time_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: refresh_tokens; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.refresh_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_providers; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.saml_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_relay_states; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.saml_relay_states ENABLE ROW LEVEL SECURITY;

--
-- Name: schema_migrations; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.schema_migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: sessions; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.sessions ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_domains; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.sso_domains ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_providers; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.sso_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: users; Type: ROW SECURITY; Schema: auth; Owner: optitab_db_user
--

ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

--
-- Name: messages; Type: ROW SECURITY; Schema: realtime; Owner: optitab_db_user
--

ALTER TABLE realtime.messages ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets; Type: ROW SECURITY; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE storage.buckets ENABLE ROW LEVEL SECURITY;

--
-- Name: migrations; Type: ROW SECURITY; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE storage.migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: objects; Type: ROW SECURITY; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads; Type: ROW SECURITY; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE storage.s3_multipart_uploads ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads_parts; Type: ROW SECURITY; Schema: storage; Owner: optitab_db_user
--

ALTER TABLE storage.s3_multipart_uploads_parts ENABLE ROW LEVEL SECURITY;

--
-- Name: supabase_realtime; Type: PUBLICATION; Schema: -; Owner: optitab_db_user
--

CREATE PUBLICATION supabase_realtime WITH (publish = 'insert, update, delete, truncate');


ALTER PUBLICATION supabase_realtime OWNER TO optitab_db_user;

--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: optitab_db_user
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: FUNCTION armor(bytea); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.armor(bytea) TO optitab_db_user;


--
-- Name: FUNCTION armor(bytea, text[], text[]); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.armor(bytea, text[], text[]) TO optitab_db_user;


--
-- Name: FUNCTION crypt(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.crypt(text, text) TO optitab_db_user;


--
-- Name: FUNCTION dearmor(text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.dearmor(text) TO optitab_db_user;


--
-- Name: FUNCTION decrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION decrypt_iv(bytea, bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION digest(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.digest(bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION digest(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.digest(text, text) TO optitab_db_user;


--
-- Name: FUNCTION encrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION encrypt_iv(bytea, bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION gen_random_bytes(integer); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.gen_random_bytes(integer) TO optitab_db_user;


--
-- Name: FUNCTION gen_random_uuid(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.gen_random_uuid() TO optitab_db_user;


--
-- Name: FUNCTION gen_salt(text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.gen_salt(text) TO optitab_db_user;


--
-- Name: FUNCTION gen_salt(text, integer); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.gen_salt(text, integer) TO optitab_db_user;


--
-- Name: FUNCTION grant_pg_graphql_access(); Type: ACL; Schema: extensions; Owner: optitab_db_user
--

GRANT ALL ON FUNCTION extensions.grant_pg_graphql_access() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION hmac(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.hmac(bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION hmac(text, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.hmac(text, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) TO optitab_db_user;


--
-- Name: FUNCTION pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) TO optitab_db_user;


--
-- Name: FUNCTION pgp_armor_headers(text, OUT key text, OUT value text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_key_id(bytea); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_key_id(bytea) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_encrypt(text, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_encrypt(text, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_encrypt_bytea(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) TO optitab_db_user;


--
-- Name: FUNCTION pgp_pub_encrypt_bytea(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_decrypt(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_decrypt(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_decrypt_bytea(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_decrypt_bytea(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_encrypt(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_encrypt(text, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_encrypt_bytea(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) TO optitab_db_user;


--
-- Name: FUNCTION pgp_sym_encrypt_bytea(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) TO optitab_db_user;


--
-- Name: FUNCTION pgrst_ddl_watch(); Type: ACL; Schema: extensions; Owner: optitab_db_user
--

GRANT ALL ON FUNCTION extensions.pgrst_ddl_watch() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION pgrst_drop_watch(); Type: ACL; Schema: extensions; Owner: optitab_db_user
--

GRANT ALL ON FUNCTION extensions.pgrst_drop_watch() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION set_graphql_placeholder(); Type: ACL; Schema: extensions; Owner: optitab_db_user
--

GRANT ALL ON FUNCTION extensions.set_graphql_placeholder() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION uuid_generate_v1(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_generate_v1() TO optitab_db_user;


--
-- Name: FUNCTION uuid_generate_v1mc(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_generate_v1mc() TO optitab_db_user;


--
-- Name: FUNCTION uuid_generate_v3(namespace uuid, name text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) TO optitab_db_user;


--
-- Name: FUNCTION uuid_generate_v4(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_generate_v4() TO optitab_db_user;


--
-- Name: FUNCTION uuid_generate_v5(namespace uuid, name text); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) TO optitab_db_user;


--
-- Name: FUNCTION uuid_nil(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_nil() TO optitab_db_user;


--
-- Name: FUNCTION uuid_ns_dns(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_ns_dns() TO optitab_db_user;


--
-- Name: FUNCTION uuid_ns_oid(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_ns_oid() TO optitab_db_user;


--
-- Name: FUNCTION uuid_ns_url(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_ns_url() TO optitab_db_user;


--
-- Name: FUNCTION uuid_ns_x500(); Type: ACL; Schema: extensions; Owner: postgres
--

GRANT ALL ON FUNCTION extensions.uuid_ns_x500() TO optitab_db_user;


--
-- Name: TABLE schema_migrations; Type: ACL; Schema: auth; Owner: optitab_db_user
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.schema_migrations TO postgres;
GRANT SELECT ON TABLE auth.schema_migrations TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO optitab_db_user;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO optitab_db_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO optitab_db_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO optitab_db_user;


--
-- PostgreSQL database dump complete
--

