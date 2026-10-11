-- Export du jeu « communes-velo.csv » : une ligne par commune de France métropolitaine.
-- Entrées (dans le répertoire courant) : lineaire-com.csv (Géovélo), fub_*.csv (FUB 2025 par région), insee.csv (Insee RP : population, mode de transport).
SET memory_limit='1200MB';
create or replace table lin as
  select code_com::varchar code, annee::int annee, type_amenagement t, numerateur::double km, denominateur::double pop_g
  from read_csv_auto('lineaire-com.csv', types={'code_com':'VARCHAR'});
create or replace table fub as
  select * from read_csv_auto('fub_*.csv', union_by_name=true, types={'insee':'VARCHAR','departement':'VARCHAR'});
create or replace table ins as
  select code::varchar code, nom, pop, bike, car, tc, walk, nonem, moto
  from read_csv_auto('insee.csv', types={'code':'VARCHAR'});

-- Paris, Lyon, Marseille : l'Insee publie par arrondissement, on additionne pour la ville entière
create or replace table villes as
  select case when code like '751%' then '75056' when code like '6938%' then '69123' else '13055' end code,
         sum(bike) bike, sum(car) car, sum(tc) tc, sum(walk) walk, sum(nonem) nonem, sum(moto) moto
  from ins where (code like '751__' and code<>'75056') or code like '6938_' or code like '132__' group by 1;
create or replace table ins2 as
  select code, bike, car, tc, walk, nonem, moto from ins where code not in (select code from villes)
  union all select code, bike, car, tc, walk, nonem, moto from villes;

create or replace table g as
  select code, max(case when annee=2025 then pop_g end) population,
         round(sum(case when annee=2025 then km end),2) km_total_2025,
         round(sum(case when annee=2025 and t='pistes cyclables' then km end),2) km_pistes,
         round(sum(case when annee=2025 and t='voies vertes' then km end),2) km_voies_vertes,
         round(sum(case when annee=2025 and t='bandes cyclables' then km end),2) km_bandes,
         round(sum(case when annee=2025 and t='double-sens cyclables' then km end),2) km_double_sens,
         round(sum(case when annee=2025 and t='voies bus partagées' then km end),2) km_voies_bus,
         round(sum(case when annee=2025 and t='aménagements mixtes' then km end),2) km_mixtes,
         round(sum(case when annee=2025 and t='autre' then km end),2) km_autre,
         round(sum(case when annee=2022 then km end),2) km_total_2022
  from lin group by 1;

copy (
  select g.code code_insee,
         coalesce(i.nom, f.nom) nom,
         g.population::int population,
         g.km_total_2025, g.km_pistes, g.km_voies_vertes, g.km_bandes, g.km_double_sens, g.km_voies_bus, g.km_mixtes, g.km_autre, g.km_total_2022,
         round(1000*g.km_total_2025/nullif(g.population,0),3) km_pour_1000_hab,
         round(1000*(g.km_pistes+g.km_voies_vertes)/nullif(g.population,0),3) km_proteges_pour_1000_hab,
         round(100*s.bike/nullif(s.bike+s.car+s.tc+s.walk+s.nonem+s.moto,0),2) part_velo_domicile_travail_pct,
         f.categorie fub_categorie, round(f.score,3) fub_score, f.classe fub_classe,
         round(f.ressenti,3) fub_ressenti, round(f.securite,3) fub_securite, round(f.confort,3) fub_confort,
         round(f.efforts,3) fub_efforts, round(f.services,3) fub_services,
         round(f.score_2019,3) fub_score_2019, round(f.score_2021,3) fub_score_2021,
         try_cast(f."evolution_2021-2025" as double) fub_evolution_2021_2025
  from g left join ins2 s using(code)
       left join (select code, nom from ins) i using(code)
       left join fub f on f.insee=g.code
  order by g.code
) to 'communes-velo.csv' (header, delimiter ',');
select count(*) n, count(fub_score) with_fub, count(part_velo_domicile_travail_pct) with_modal
from read_csv_auto('communes-velo.csv', types={'code_insee':'VARCHAR'});
