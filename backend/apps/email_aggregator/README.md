Email aggregator allows to build and send weekly reports to users via

```poetry run python email_aggregator/commands/aggregate_views.py```

This job can be easily included in cron job on whatever server it will be executed.

Development note:

Please before running script apply **clickhouse.ddl** in docker container

For test data you can run

INSERT INTO ugc_film_views (user_id, film_id, progress_sec, timestamp) VALUES ('6e1d795d-e720-488e-9388-aa38bdb04be3', '73ee3f17-63fc-467f-b87c-3e17e6c6a341', 1, now());
INSERT INTO ugc_film_views (user_id, film_id, progress_sec, timestamp) VALUES ('6e1d795d-e720-488e-9388-aa38bdb04be3', '73ee3f17-63fc-467f-b87c-3e17e6c6a343', 2, now());
INSERT INTO ugc_film_views (user_id, film_id, progress_sec, timestamp) VALUES ('6e1d795d-e720-488e-9388-aa38bdb04be3', '73ee3f17-63fc-467f-b87c-3e17e6c6a342', 3, now());

INSERT INTO ugc_film_views (user_id, film_id, progress_sec, timestamp) VALUES ('6e1d795d-e720-488e-9388-aa38bdb04be4', '73ee3f17-63fc-467f-b87c-3e17e6c6a341', 1, now());
INSERT INTO ugc_film_views (user_id, film_id, progress_sec, timestamp) VALUES ('6e1d795d-e720-488e-9388-aa38bdb04be4', '73ee3f17-63fc-467f-b87c-3e17e6c6a343', 2, now());
INSERT INTO ugc_film_views (user_id, film_id, progress_sec, timestamp) VALUES ('6e1d795d-e720-488e-9388-aa38bdb04be4', '73ee3f17-63fc-467f-b87c-3e17e6c6a342', 3, now());