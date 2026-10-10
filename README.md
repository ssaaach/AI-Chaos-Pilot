# AI Chaos Pilot (Bosch Resilience AI)

Platform and application foundation for the Bosch Resilience AI hackathon project: a
safe, locally-run chaos engineering platform that maps a cloud-native application's
dependencies, chooses bounded failure experiments, measures their effect, and explains
the resulting weaknesses. Google Online Boutique is the application under test; a
separate synthetic PostgreSQL lab demonstrates prevention of risky queries.

Start with [the project context](CONTEXT.md), [shared interfaces](contracts/INTERFACES.md),
[platform status](docs/platform/README.md), and [telemetry status](docs/telemetry/README.md).

## Local setup

Requires Python 3.11+, Docker Desktop (hosts the kind nodes), `kubectl`, and `kind`.

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# POSIX:    source .venv/bin/activate
pip install -r requirements.txt
```

`pydantic` is required by the backend models. `httpx` and `psycopg` are lazy imports
needed only for live runs (the Online Boutique probe and PostgreSQL `EXPLAIN`); the
unit suite passes without them.

## Verify the checkout

```bash
python -m unittest discover -s tests/telemetry -t .      # 109 tests
python scripts/telemetry/run_prevention_acceptance.py    # writes reports/local_demo_prevention.json
```

Neither is a live measurement. Every fixture is `Source.FIXTURE`, and the prevention
run exercises a loopback harness, not a deployed cluster.

## Cluster work

Docker Desktop must be running first. Cluster creation is explicit and opt-in:

```powershell
scripts/platform/setup-cluster.ps1 -CreateCluster
scripts/platform/enroll.ps1  -Context kind-bosch-ananya
scripts/platform/audit.ps1   -Context kind-bosch-ananya
```

See [docs/platform/README.md](docs/platform/README.md) for enrollment and teardown
semantics, including why a destructive teardown requires an explicit cluster name.

## Status

This workspace contains **no** pinned Online Boutique checkout evidence and **no** live
cluster evidence. Fixture data is labeled as synthetic. Do not treat it as deployment
output. `docs/telemetry/README.md` lists exactly what is and is not yet proven.

## Third-party code

`application/online-boutique/` vendors [Google's Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo)
(Apache-2.0). Its upstream license and notices are preserved in that directory.
