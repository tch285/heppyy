#!/usr/bin/env python3

from __future__ import print_function
import tqdm
import argparse
import os
import numpy as np
import heppyy
from heppyy.pythia_util import configuration as pyconf

_ = heppyy.load_cppyy('heppyy')
Pythia8 = heppyy.load_cppyy('pythia8.Pythia8')
fj = heppyy.load_cppyy('fastjet')
std = heppyy.load_cppyy('std')

def main():
	parser = argparse.ArgumentParser(description='pythia8 fastjet on the fly', prog=os.path.basename(__file__))
	pyconf.add_standard_pythia_args(parser)
	parser.add_argument('--ignore-mycfg', help="ignore some settings hardcoded here", default=False, action='store_true')
	parser.add_argument('-v', '--verbose', help="be verbose", default=False, action='store_true')
	args = parser.parse_args()

	pythia = Pythia8.Pythia()

	fj.ClusterSequence.print_banner()
	print()
	# set up our jet definition and a jet selector
	jet_R0 = 0.4
	jet_def = fj.JetDefinition(fj.antikt_algorithm, jet_R0)
	jet_selector = fj.SelectorPtMin(100.0) * fj.SelectorAbsEtaMax(1)
	print(jet_def)

	jet_def_lund = fj.JetDefinition(fj.cambridge_algorithm, 1.0)
	lund_gen = fj.contrib.LundGenerator(jet_def_lund)
	print('making lund diagram for all jets...')
	print(f' {lund_gen.description()}')

	mycfg = ['PhaseSpace:pThatMin = 100']
	if args.ignore_mycfg:
		mycfg = []
	pythia = pyconf.create_and_init_pythia_from_args(args, mycfg)
	if not pythia:
		print("[e] pythia initialization failed.")
		return
	if args.nev < 10:
		args.nev = 10
	for i in tqdm.tqdm(range(args.nev)):
		if not pythia.next():
			continue
		parts = std.vector[fj.PseudoJet]([fj.PseudoJet(p.px(), p.py(), p.pz(), p.e()) for p in pythia.event if p.isFinal()])
		# parts = pythiafjext.std.vectorize(pythia, True, -1, 1, False)
		jets = jet_selector(jet_def(parts))
		print(f'number of jets: {len(jets)} from n parts: {len(parts)}')
		# pythiafjtools.pythia_fastjet_test(pythia)
		_info = Pythia8.getInfo(pythia)
		#print(f'from info: {_info.code()} {_info.sigmaGen()} {_info.sigmaErr()}')
		# pythia.info.list() # defunct in cppyy use Pythia8.getInfo(pythia) instead
		# _info.list()
		for j in jets:
			groom_shop = fj.contrib.GroomerShop(j, fj.cambridge_algorithm)
			max_kt = groom_shop.max_kt()
			lunds = lund_gen.result(j)
			if args.verbose:
				print(f'jet pT={j.perp()} sigmaGen={_info.sigmaGen()}')
			if args.verbose:
				for i, l in enumerate(lunds):
					print('- L {} pT={:5.2f} eta={:5.2f}'.format(i, l.pair().perp(), l.pair().eta()))
					print('  Delta={}'.format(l.Delta()))
					print('  kt={}'.format(l.kt()), 'is max kT?', l.kt() == max_kt.kt())
					print()


	pythia.stat()

	print(type(pythia))


if __name__ == '__main__':
	main()
