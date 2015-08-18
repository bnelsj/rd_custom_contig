from optparse import OptionParser
from pygr import *

from pygr import worldbase
import pygr
from pygr.seqdb import SequenceFileDB

import numpy as np


if __name__=="__main__":
	opts = OptionParser()
	opts.add_option('','--input_fasta',dest='input_fasta',default=None)
	opts.add_option('','--output_fastq',dest='output_fastq',default=None)
	opts.add_option('','--ignore_masked_bases',dest='ignore_masked_bases',action='store_true',default=False)
	opts.add_option('','--mask_in_input',dest='mask_in_input',action='store_true',default=False)
	opts.add_option('','--kmer_len',dest='kmer_len',default=30,type=int)
	(o,args) = opts.parse_args()

	input_fa_RM = "%s.masked"%(o.input_fasta)
	input_fa_TRF = "%s.2.3.5.80.10.30.1000.mask"%(o.input_fasta) ####CHANGE THIS TO PROPER MASKING!

	input_fa = SequenceFileDB(o.input_fasta)
	if not o.ignore_masked_bases:
		input_fa_RM = SequenceFileDB(input_fa_RM)
		input_fa_TRF = SequenceFileDB(input_fa_TRF)

	#$if len(input_fa)>1: 
	#	print "more than one contig in loaded fasta..."
	#	sys.exit(1)

	for seq in input_fa:
		contig_name =  seq

		###########IN THIS SAME WAY, I COULD REMOVE POLY G/A/T/C tracks....??? FORGET FOR NOW
		if not o.ignore_masked_bases:
			char_fa_RM = np.array(str(input_fa_RM[contig_name]),'c')
			char_fa_TRF = np.array(str(input_fa_TRF[contig_name]),'c')
			masked = (char_fa_RM=="N")|(char_fa_TRF=="N")
		elif o.mask_in_input:
			char_input_fa = np.array(str(input_fa[contig_name]),'c')
			masked = char_input_fa=="N"
		else:
			masked = np.zeros(len(input_fa[contig_name]))

		kernel = np.ones(o.kmer_len)
		conv = np.convolve(masked,kernel,'valid')	
		qual_str = "".join(["0" for i in xrange(o.kmer_len)])

		for i in xrange(len(input_fa[contig_name])-o.kmer_len):
			if conv[i]==0:
				#print "@%s_%i"%(contig_name,i)
				print "%s\t%d\t%d\t%s"%(contig_name,i,i+o.kmer_len,input_fa[contig_name][i:i+o.kmer_len])
				#print "+"
				#print qual_str 
				#print conv[i], input_fa_RM[contig_name][i:i+o.kmer_len]





