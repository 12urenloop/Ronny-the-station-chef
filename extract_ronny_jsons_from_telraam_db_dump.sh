#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ $# -ne 1 ]; then
    echo "Usage: ${0} telraam_db_dump.sql(.tar)"
    echo "Note: Make sure to gunzip the dump first."
    exit 1
fi

export POSTGRES_USER=telraam_user
export POSTGRES_DB=telraam_dev
export POSTGRES_DUMP_FILE="${1}"

podman run --rm -i -v"${PWD}:/work" -w/work docker.io/library/postgres:18.3 bash -c "
set -euo pipefail
cat >/tmp/dump.sql.tar
[ \$(wc -c </tmp/dump.sql.tar) -gt 0 ]

echo \"Starting postges...\"
export POSTGRES_USER=$POSTGRES_USER
export POSTGRES_HOST_AUTH_METHOD=trust
docker-entrypoint.sh postgres &>/dev/null &
sleep 5

echo \"Restoring dump...\"
pg_restore -U$POSTGRES_USER -dpostgres -cC 1>&2 </tmp/dump.sql.tar &>/dev/null || true

psql -U$POSTGRES_USER -d$POSTGRES_DB -c\"
    SELECT * FROM station;
\"

mkdir -p ronny
for i in \$(seq 1 8); do
    name=\$(printf \"ronny%02d\" \$i)
    echo \"Exporting detections for \$name\"
    psql -U$POSTGRES_USER -d$POSTGRES_DB -tA -c\"
        WITH subquery AS (
            SELECT
                detection.remote_id AS id,
                detection.timestamp AS detection_timestamp,
                baton.mac AS mac,
                detection.rssi AS rssi,
                detection.uptime_ms AS uptime_ms,
                detection.battery AS battery
            FROM detection
            LEFT JOIN baton ON detection.baton_id = baton.id
            LEFT JOIN station ON detection.station_id = station.id
            WHERE station.name = '\$name'
            ORDER BY detection.remote_id ASC
            LIMIT NULL
        )
        SELECT json_agg(subquery) FROM subquery;
    \" >ronny/\$name.json
done

kill %1
" <"${POSTGRES_DUMP_FILE}"
