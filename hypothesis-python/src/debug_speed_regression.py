#! /usr/bin/python3
import sys
import os
import time

import hypothesis.strategies as st
from hypothesis import Phase, given, settings

MAX_EXAMPLES = int(os.getenv("MAX_EXAMPLES", "60"))

def gen_empty_fingerprint():
  return {i: {} for i in range(8)}

@settings(max_examples=MAX_EXAMPLES, deadline=None,
        phases=(Phase.reuse, Phase.generate, Phase.shrink))
@given(data=st.data())
def get_fuzzy_car_interfaces(data):
  fingerprint_strategy = st.fixed_dictionaries({key: st.dictionaries(st.integers(min_value=0, max_value=0x800),
                                                                     st.integers(min_value=0, max_value=64)) for key in
                                                gen_empty_fingerprint()})
  # TODO: Add another st.fixed_dictionaries()
  data.draw(fingerprint_strategy)

if __name__ == "__main__":
  # first bad commit: 5de1fe84252051594fdc6879d4920c357a6d1368 - more likely to generate boundary values
  # from 3.5 - 3.8s:  6e2f394a253761677cdcc0990a32df54a62f079a
  #     - better after revert: 6e2f394a253761677cdcc0990a32df54a62f079a
  # from 4s - >5s: 1e76ce2e52e450d54470ed09b9c65fb1b598fb5c - trackIRTree in ConjectureData

  lower = float(sys.argv[1])
  higher = float(sys.argv[2])

  num_iterations = 20
  start = time.monotonic()
  for _ in range(num_iterations):
    get_fuzzy_car_interfaces()

  print(f"{num_iterations} iterations takes {time.monotonic() - start}s")
  time_taken = time.monotonic() - start
  sys.exit(int(lower <= time_taken <= higher))
