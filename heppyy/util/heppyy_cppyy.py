import yasp
import cppyy

headers = [
	"eec/ecorrel.hh",
	"fjutil/fjutil.hh",
	"fjext/fjtools.hh",
	"groom/GroomerShop.hh",
	"pythiaext/PythiaExt.hh",
	"hybridutil/readhybrid.hh",
	"hybridutil/hybridNegaRecombiner.hh"
 ]
packs = ['heppyy']
libs = ['heppyy_eec', 'heppyy_fjutil', 'heppyy_fjext', 'heppyy_groom', 'heppyy_pythiafjext', 'heppyy_pythiaext', 'heppyy_hybridutil']

from yasp.cppyyhelper import YaspCppyyHelper
YaspCppyyHelper().load(packs, libs, headers)
print(YaspCppyyHelper())

