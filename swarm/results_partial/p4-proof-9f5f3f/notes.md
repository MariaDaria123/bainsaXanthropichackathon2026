# notes (not seen by critics)
- Started 15:23. Task premise (l>=4 handled by omega collision for k<=210) checked: false, counting does not force collision. table.py.
- Tried: fiber reduction (Claim 3) - gives disjoint family of size k-l+1 but gcds only < k, not < k-l+1, so minimality gives nothing directly.
- Tried: deletion lemma G_t cascade from t=k-1 downward for k=32, l=3: gives |D_30|>=2, then D_29 etc.; union of linear cliques always coverable as t drops, no contradiction found by hand.
- Toy config m_s=31*{2,3,5}, all others 30: killed by parity (only 15 residues mod 30 of fixed parity vs 29 classes). Suggests density/fiber arguments may help for specific shapes, not general.

## Round 1 revision
Both critics MINOR. Fixed: Claim 1 now marked conditional on F1-F3; "premise false" reworded (the collision premise is true, only the pigeonhole fails); l=3 rows marked as "test not applicable"; Claim 3 consequence marked conditional; M4 remark added. It turned out equal to Claim 4(a) on {s} plus R, so there is no gain; the cert.py hygiene issue is noted.
