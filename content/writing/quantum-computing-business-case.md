---
title: "Quantum computing's honest business case in 2026"
date: 2026-04-11
description: "A calibrated assessment of where quantum computing will deliver business value, when, and where the current hype substantially exceeds the underlying technical reality."
tags: [writing, quantum-computing, business-strategy]
draft: false
---

Quantum computing in 2026 occupies a curious position. It is technically real in ways it was not ten years ago, and it is commercially overhyped in ways that are difficult to assess without both deep technical understanding and sustained attention to specific hardware roadmaps. The gap between what the industry claims and what the physics actually supports has widened over the past three years. Separating the two requires effort most business leaders cannot afford to make. The result is that capital and strategic attention are being allocated on the basis of misleading signals.

I have been following quantum computing since my theoretical-physics background first overlapped with the research community in the mid-2000s. My research notes library covers the technical details in depth. This essay is the business-facing summary of where I think the field actually is, when business value will arrive by vertical, and how I would advise a firm evaluating its quantum-computing investment.

I will be specific about time horizons. Vague framings ("soon," "in the next decade") are not useful for capital allocation. I commit to specific ranges with specific conditions.

## What is provably real

Three quantum speedups are provable, meaning they have mathematical proofs against classical lower bounds or substantial theoretical foundations.

### Shor's algorithm for factoring

Shor (1995) factors an $N$-bit integer in $O((\log N)^3)$ quantum operations. The best classical algorithm (general number field sieve) takes sub-exponential but super-polynomial time. For RSA-2048, the gap between classical and quantum is substantial. No one expects classical progress to close it before the hardware allows Shor to run.

The catch. Running Shor on RSA-2048 requires approximately 20 million physical qubits operating with physical error rate around $10^{-3}$, per Gidney-Ekerå (2021). Current hardware has on the order of 1000 physical qubits (IBM Condor, Quantinuum H2). The four-order-of-magnitude gap will take sustained engineering work to close.

Realistic timeline. A cryptographically relevant quantum computer for RSA-2048 is 10-15 years away. This is the consensus view among the serious researchers I know, and it has been stable for several years. Forecasts in the 5-year range are not supported by the physics. Forecasts in the 20-plus year range are overly pessimistic given the recent error-correction progress (Google Willow 2024).

**Business implication.** Every firm relying on RSA-2048 or ECC cryptography for data protection should have post-quantum cryptography migration underway now. NIST finalized ML-KEM and ML-DSA standards in 2024. The migration is a multi-year infrastructure project. Harvest-now-decrypt-later adversary scenarios are a real concern for data with multi-decade sensitivity horizons.

### Grover's algorithm for unstructured search

Grover (1996) finds a marked element in an unsorted database of $N$ items using $O(\sqrt N)$ queries, compared to $\Theta(N)$ classically. The BBBV 1997 lower bound proves Grover is optimal.

For NP-hard combinatorial optimization, Grover provides a quadratic speedup over brute-force enumeration, from $2^n$ to $2^{n/2}$. This sounds useful but is not meaningful for real problems. Classical heuristics (branch and bound, SDP, local search) already solve structured instances exponentially faster than $2^n$. Grover on top of brute force does not change the picture.

**Business implication.** Grover is not a significant business tool for optimization. Do not make strategic investments based on Grover-for-NP-hard.

### Quantum Monte Carlo for amplitude estimation

Montanaro (2015) proved that quantum amplitude estimation gives a quadratic speedup on Monte Carlo estimation. Accuracy $\varepsilon$ requires $O(1/\varepsilon)$ queries rather than $O(1/\varepsilon^2)$ classical samples. This is the only provable quantum-ML advantage that has survived dequantization attacks.

Applications include financial derivatives pricing, tail-risk estimation, and Value-at-Risk for complex portfolios. Stamatopoulos et al. (2020) demonstrated option-pricing applications. Chakrabarti et al. (2021) showed applications to credit-risk modeling.

The catch. Amplitude estimation at basis-point accuracy ($\varepsilon = 10^{-4}$) requires circuit depth on the order of $10^4$. At current NISQ error rates, this depth is not feasible. The quadratic speedup is a fault-tolerance-regime result. NISQ hardware delivers only loose approximations.

Realistic timeline. Quantum Monte Carlo for financial risk is plausibly deployable in the 2030s once the Megaquop machine arrives (Preskill 2025). Specific deployment depends on the speed of error-correction progress. The progress is being demonstrated at small scale (Willow 2024) but has not yet been demonstrated at the scale required for meaningful financial applications.

**Business implication.** For firms with large-scale derivative pricing or tail-risk estimation workloads, the 2030s bring a potential cost-structure change. Whether this is strategic enough to justify early investment depends on the firm's risk-management budget and compute infrastructure. My view is that financial firms should have a quantum-computing staff allocation (two to five scientists) tracking the space but not making large strategic bets. The timeline is too long for current financial-sector capital budgets to absorb.

## What is not provably real but heavily promoted

### QAOA for combinatorial optimization

Farhi-Goldstone-Gutmann's QAOA (2014) has been heavily promoted as a route to quantum advantage for combinatorial optimization. On theoretical grounds, at $p=1$ it achieves 0.6924 approximation ratio on 3-regular Max-Cut. Goemans-Williamson's classical SDP achieves 0.8786. QAOA at $p=1$ does not beat classical.

At higher $p$, QAOA's theoretical performance improves. The Harrigan/Arute 2020 paper in Nature Physics, authored by essentially the entire Google Quantum AI team including Farhi himself, demonstrated that on Sycamore hardware, QAOA loses to efficient classical algorithms on any problem that does not match the native hardware graph. The paper is unambiguous. QAOA does not deliver business value on real combinatorial optimization problems.

**Business implication.** Do not invest in QAOA as a path to commercial value. The physics does not support it. Firms that have built QAOA-based "quantum optimization" product claims are, at best, ahead of the technology and at worst misleading their customers.

### Quantum annealing (D-Wave)

D-Wave has shipped quantum annealers since 2011 and has been the subject of ongoing debate about whether they provide genuine quantum speedup. The Rønnow et al. 2014 Science paper showed D-Wave 2X provided at most constant-factor speedup over carefully-tuned simulated annealing. Subsequent generations (5000-qubit Advantage2) have made similar claims and attracted similar classical counterattacks.

The consensus view: D-Wave is useful physics hardware for spin-glass simulation and certain restricted Ising problems. It can be a modest accelerator for narrow use cases. It is not a general-purpose optimization accelerator. The claims that it is should be evaluated with skepticism.

**Business implication.** For most optimization workloads, D-Wave is not competitive with classical optimization methods. Specific firms (Volkswagen traffic routing, certain logistics problems) have found constant-factor speedups on structured subsets. For most firms, the ROI is negative.

### Variational quantum chemistry

VQE (Peruzzo-McClean 2013) has been the most-promoted NISQ-era quantum application. For computing ground-state energies of small molecules, it has been demonstrated on real hardware. For scaling to molecules of practical interest (protein complexes, catalysis, materials), the depth requirements run into barren-plateau territory (McClean et al. 2018) and fidelity constraints that NISQ hardware does not satisfy.

The fundamental problem: classical methods (DFT, CCSD(T), DMRG) are good and getting better. A quantum method needs to beat them at the relevant molecular scale. Current quantum methods cannot do so on fault-intolerant hardware.

Realistic timeline. Useful quantum chemistry on error-corrected hardware is plausibly 2030s. Business value depends on which specific chemistry problems remain classically intractable in that horizon. This is itself an open question because classical methods continue to improve.

**Business implication.** Pharma and materials firms should track quantum chemistry but not commit large resources yet. The classical-quantum boundary is unclear, and the timeline for quantum advantage on specific problems is longer than typical R&D planning horizons.

## Supremacy claims and what they signify

The 2019 Sycamore supremacy claim (Arute et al., Nature) was widely misinterpreted. The experiment demonstrated sampling from a specific random quantum circuit, not useful computation. Subsequent classical simulation attacks (Huang et al. 2020, Liu et al. 2021 Sunway) reduced the classical cost from an estimated 10,000 years to approximately 1 week, effectively collapsing the supremacy claim.

The 2020 Jiuzhang boson-sampling experiment (Zhong et al., Science) has held up better against classical counterattacks. The 2025 Jiuzhang 4.0 result extends the quantum advantage to programmable photonic systems with 3050 photon clicks. Again, this is sampling, not useful computation. No optimization, no factoring, no machine learning.

Supremacy experiments are scientifically interesting as demonstrations that quantum devices can do specific tasks faster than classical simulation. They are not business-relevant demonstrations. A firm making investment decisions based on supremacy headlines is making decisions on the wrong signal.

## The fault-tolerance roadmap

Every scalable quantum application requires quantum error correction. The roadmap markers.

**Threshold demonstration.** Physical qubits with error rate below the fault-tolerance threshold (around $10^{-2}$ for surface codes). This has been achieved. Per-gate error rates around $10^{-3}$ are routine on Google Willow and IBM Heron hardware.

**Distance-5 and distance-7 surface codes.** Demonstrated at small scale (Google Willow 2024). This is the first genuine step toward scalable error correction.

**Logical qubit with good error rate.** Approximately distance-15 to distance-30 surface codes, requiring roughly 1000-10,000 physical qubits per logical qubit. Plausibly 3-5 years away.

**Megaquop machine.** Preskill's 2025 benchmark of at least $10^6$ error-corrected logical operations. This is the scale at which useful quantum applications become feasible. Plausible timeline: 5-10 years for small-scale Megaquop, longer for CRQC-class devices.

**CRQC for RSA-2048.** Per Gidney-Ekerå, requires approximately 20 million physical qubits. Timeline: 10-15 years is the mainstream estimate.

**For capital allocation.** The realistic horizon for widespread quantum-computing business value is the 2030s, not the 2020s. Firms promising production quantum advantage by 2028 are either ahead of the hardware curve or selling the hype.

## How I would advise a firm evaluating quantum investment

### Cryptography and data-protection firms

This is the most urgent category. Every firm relying on pre-quantum cryptography for data protection should have an active post-quantum migration program now. The CRQC threat is 10-15 years out. The migration is a multi-year infrastructure project. Adversaries can harvest data now and decrypt later. This is not speculation. It is the current NSA, GCHQ, and NIST guidance.

Specific actions. Begin the migration to NIST-standardized post-quantum algorithms (ML-KEM, ML-DSA). Inventory data assets with multi-decade sensitivity. Establish crypto-agility infrastructure to enable rapid algorithm swap in the future.

### Financial services firms

Quantum Monte Carlo has a plausible 2030s deployment horizon for risk management and exotic-derivative pricing. A two-to-five-scientist team tracking the space is a reasonable investment for firms with more than $10 billion in risk-management budget. Larger bets are not yet justified.

Parallel investment in classical variance-reduction techniques is probably higher ROI in the near term. Quantum Monte Carlo's quadratic speedup is attractive only once classical variance reduction has been fully exploited. Most firms have not reached that point.

### Pharma, materials, and chemistry firms

Quantum chemistry may deliver value in the 2030s on specific molecular-simulation problems. Research partnerships with quantum-hardware vendors to characterize the classical-quantum boundary on firm-specific problems are low-cost insurance. Substantial capital commitments are premature.

### Industrial logistics and operations firms

QAOA and quantum annealing are not delivering commercial value. Do not invest based on vendor promises of imminent optimization advantage. The claims are not consistent with the physics.

If you operate optimization problems that might benefit from modest accelerators, D-Wave's Advantage system might be useful for specific structured workloads. Treat it as a narrow tool, not a general-purpose accelerator.

### AI and ML firms

Most "quantum ML" claims have been dequantized (Tang 2018 onward). The exceptions are quantum Monte Carlo and specific simulation problems. Generic quantum-ML investment is not yet justified by evidence. Specific applications in simulation or finance may be.

## The strategic framework I would use

For a board evaluating quantum computing investment, the simple framework.

1. **Post-quantum cryptography migration.** Yes, now. This is necessary regardless of other quantum investment.
2. **Monitoring and research engagement.** Yes, at modest scale (two to five full-time-equivalent people) for firms with more than $1 billion revenue in relevant verticals.
3. **Hardware procurement.** Defer to 2028 or later unless there is a specific workload that justifies it.
4. **Specific application development.** Probably 2030 and later for most commercial applications. Specific use cases in cryptanalysis (defensive) and risk management may come earlier.
5. **Strategic acquisitions in the space.** Only at modest valuations. The sector is overcapitalized relative to the underlying technical progress. Valuations are due for correction.

A board that makes decisions on this framework will be substantially less exposed to hype-cycle risk than one that commits to large quantum-computing capital on the basis of vendor promises. The technology is genuinely advancing. The business case timing is much later than the discourse suggests.

## Personal view

I have been long-optimistic on quantum computing for fifteen years and remain so. The physics works. The engineering is improving. The 2030s and 2040s will bring genuine quantum-advantage applications that will reshape parts of finance, cryptography, chemistry, and logistics.

The 2020s will not. The capital currently flowing into quantum computing is, in my view, substantially overweighted relative to the realistic timeline. Some of it will be clawed back through disappointment-driven valuation corrections over the next five years. The firms that end up owning the eventual commercial advantage will not be the ones that made the loudest claims in 2023-2026. They will be the ones that invested systematically in foundational research and hardware scaling, ignored the hype cycles, and were ready when the Megaquop machine arrived.

As someone who would lead research work in this space, my approach would be exactly this. Invest in the foundational work. Hedge against both too-fast and too-slow timelines. Be disciplined about when to commit capital and when to wait. Quantum computing is a real technology on a long timeline. Treat it as such.

---

*Comments and corrections welcome at iohanngrig@gmail.com. I am particularly interested in cases where I have been too conservative about specific applications I may have overlooked.*
