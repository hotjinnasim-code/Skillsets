# Delivery regression execution

Command: `python3 -B -m unittest discover -s skills/ducttape-poster/tests -p test_prepare_delivery.py -v` from `Skillsets`.

All subprocess Python calls use `-B`; every test temporary directory is explicitly created inside the Ducttape Poster task directory and removed by unittest cleanup. Fixtures are synthetic valid tiny PNGs built with standard-library struct/zlib. No image generation, network, dependency installation, remote reference probe, or visual/style evaluation was performed.

Coverage: five selected cards and original/dimension pairing; single edit; NONE partial; mixed transport failure; missing/null/opaque dialog refs; explicitly simulated refs with source/remote unverified; unreadable optional source; thumbnail/earlier-revision byte mismatch; corrupt source; dimensions mismatch; unsafe refs; duplicate/count/schema errors; NONE image fields; no overwrite; bad local display.

Exit code: 0. Full test output: `unittest-output.txt`.
