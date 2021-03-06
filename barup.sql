PGDMP         /            
    v           barup    10.4    10.4     O           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            P           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            Q           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            R           1262    41528    barup    DATABASE     w   CREATE DATABASE barup WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
    DROP DATABASE barup;
             luismartinezperaza    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            S           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    13253    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            T           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    42297    inventory_check    TABLE     �   CREATE TABLE public.inventory_check (
    id integer NOT NULL,
    approx_level double precision,
    weight double precision,
    purchase_id integer NOT NULL,
    date_consumed date,
    date_measured date
);
 #   DROP TABLE public.inventory_check;
       public         postgres    false    3            �            1259    42295    inventory_check_id_seq    SEQUENCE     �   CREATE SEQUENCE public.inventory_check_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.inventory_check_id_seq;
       public       postgres    false    201    3            U           0    0    inventory_check_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.inventory_check_id_seq OWNED BY public.inventory_check.id;
            public       postgres    false    200            �            1259    42273    product    TABLE     k  CREATE TABLE public.product (
    id integer NOT NULL,
    brand character varying(50),
    name character varying(50),
    bottle_weight double precision,
    vintage integer,
    label_name character varying(50),
    country character varying(50),
    volume character varying(50),
    category character varying(50),
    description character varying(2000)
);
    DROP TABLE public.product;
       public         postgres    false    3            �            1259    42271    product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.product_id_seq;
       public       postgres    false    197    3            V           0    0    product_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;
            public       postgres    false    196            �            1259    42284    purchase    TABLE     �   CREATE TABLE public.purchase (
    id integer NOT NULL,
    quantity integer,
    price double precision,
    product_id integer NOT NULL,
    purchase_date date
);
    DROP TABLE public.purchase;
       public         postgres    false    3            �            1259    42282    purchase_id_seq    SEQUENCE     �   CREATE SEQUENCE public.purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.purchase_id_seq;
       public       postgres    false    3    199            W           0    0    purchase_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.purchase_id_seq OWNED BY public.purchase.id;
            public       postgres    false    198            �           2604    42300    inventory_check id    DEFAULT     x   ALTER TABLE ONLY public.inventory_check ALTER COLUMN id SET DEFAULT nextval('public.inventory_check_id_seq'::regclass);
 A   ALTER TABLE public.inventory_check ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    200    201    201            �           2604    42276 
   product id    DEFAULT     h   ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);
 9   ALTER TABLE public.product ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    197    196    197            �           2604    42287    purchase id    DEFAULT     j   ALTER TABLE ONLY public.purchase ALTER COLUMN id SET DEFAULT nextval('public.purchase_id_seq'::regclass);
 :   ALTER TABLE public.purchase ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    198    199    199            L          0    42297    inventory_check 
   TABLE DATA               n   COPY public.inventory_check (id, approx_level, weight, purchase_id, date_consumed, date_measured) FROM stdin;
    public       postgres    false    201   '!       H          0    42273    product 
   TABLE DATA               ~   COPY public.product (id, brand, name, bottle_weight, vintage, label_name, country, volume, category, description) FROM stdin;
    public       postgres    false    197   �!       J          0    42284    purchase 
   TABLE DATA               R   COPY public.purchase (id, quantity, price, product_id, purchase_date) FROM stdin;
    public       postgres    false    199   o&       X           0    0    inventory_check_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.inventory_check_id_seq', 23, true);
            public       postgres    false    200            Y           0    0    product_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.product_id_seq', 9, true);
            public       postgres    false    196            Z           0    0    purchase_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.purchase_id_seq', 22, true);
            public       postgres    false    198            �           2606    42302 $   inventory_check inventory_check_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.inventory_check
    ADD CONSTRAINT inventory_check_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.inventory_check DROP CONSTRAINT inventory_check_pkey;
       public         postgres    false    201            �           2606    42281    product product_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public         postgres    false    197            �           2606    42289    purchase purchase_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.purchase DROP CONSTRAINT purchase_pkey;
       public         postgres    false    199            �           2606    42303 0   inventory_check inventory_check_purchase_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.inventory_check
    ADD CONSTRAINT inventory_check_purchase_id_fkey FOREIGN KEY (purchase_id) REFERENCES public.purchase(id);
 Z   ALTER TABLE ONLY public.inventory_check DROP CONSTRAINT inventory_check_purchase_id_fkey;
       public       postgres    false    201    3017    199            �           2606    42290 !   purchase purchase_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);
 K   ALTER TABLE ONLY public.purchase DROP CONSTRAINT purchase_product_id_fkey;
       public       postgres    false    199    3015    197            L   y   x���Q
�0E��d/)>�4�^��u�a�J/��E=�,�E�O�SD��EV�rf_�� fs ##H9A��FкmB;A��I��A"�	� տ��6b��p?s�f����� �s� ���      H   �  x�uVQR#7��O��Na�e7�I�M�`��I�ִ=Zk����|��^N�'�Sl(
3R�����Z^��}����F����7�b����D�������2o4_Y����C��`�I�2'ii�ƭ�;��mg��H$^cc�1�ƙ~�ɯhqJ;�i|O�����N���{�E�9��HG�c$p4�� ӆ��{�S7�Vd �q`�$4�Su��%��=�	rT`�+���� ���:��c��q�S�����LBK;�O�JC?Lv��%6.���]�&��	C0;��G��&�5'��?��T4���'qm0z��{��;��n�v����[���O��\GD5�1�֤�d�c0(u�6%�9Lbmy��i)=
>
�o��~)!��K�����R掜'�Wq6��X���[8��L]v~0���\�.���O��Y��钧/��p����BB�c"��5�j�C��H�C�./�E�h�����a��Clf��%���Y�V�u�H���+���˸$.^����m$ZY�
K�q�i >��9vt�O�v��&���[�N/�J�b�t$A��o�m��æe�'�E�:hq��1=�G���#ddt��lŴ�U#򨡡d�^�y�%�/�OF��p�L�x�<����<�q(:E�3ɰ%�n��Ѥ9�(]�-��_X�/���tHV��l����U��c����|2�
�.C���$�m�S��u�j2��TO
f�#l�wUك��y���hG}Zy�m[��`E�X[���<�N��3�*��nT�/&[	xp%��$���_���
I��I�ҁ_�"Z������UL�jہ�7h?�ЙF��X�⨍+��I�(���}DCo�$�+�8��f)�:~�>H_&��������ڄ1��{�M�g�r!�eJ��w��\]��9��>A�����y����g񡲷�aլwjqN����Ty�3��-�#�]C�?_���ޤ/b'I�å��E���<z�f~A��V��o=��;�yo�tJ���V���͐reK��שֳ��
�F�df
g��R��k���X���
��P��-�DC�ˇ�1��<���7�Pc �4�ȉ�{Qff��>����B)讅���Vf��-j���#'��ò���;�O�����rn>��! ����9���%�~}(�v�|����k�G3�����9�      J   �   x���I��0D�p� &ܥ�����y�ޥ�
AUԩ5^� e���łL�7HgY��0:��\4(9'��6ʟq`+�Q+$��8.c쵑��^.�@�B��I�g�{�	
�� �Yֳlu���g�=rlr]�:E_o�c�F3��*Qyͪ-��e07**k��r���{SY�W�s�`�	
�,�dv��K��B�_ym$     