#Getting read depth for a custom contig
This page documents the snakemake pipeline for read depth analysis on a custom contig.
The basic steps are:
  - Hard mask
  - Find SUNKs
  - Map samples
  - Get WSSD combined corrected files

##Running the pipeline
```
git clone https://github.com/bnelsj/rd_custom_contig.git
cd rd_custom_contig
```

Set the variables in ''config.json'' to match your data. In particular, set ''contig'', ''contig_files[fasta]'', and ''contig_files[allelic_regions]''. Note that your fasta file may contain multiple contigs, but there is currently no support for parallelization through separating analyses by contig. Allelic regions are the coordinates in the reference genome that will be patched by your contig(s).

##Preparing your custom contig

Do a dry run to test if your snakefile is setup properly:
```
snakemake -s contig_setup_custom.snake --configfile config.json -np
```
This will build the snakemake rule graph and print shell commands, but won't run any jobs. If you aren't getting any errors, run the pipeline for real:
```
snakemake -s contig_setup_custom.snake --configfile config.json -c "qsub {params.sge_opts}" -j 5 -w 30
```

This will hard mask using RepeatMasker and TRF, build a patched, hard masked reference, find unique kmers in your contigs, and remove unique kmers found elsewhere in the reference to build a SUNK dts file.

##Read depth mapping with mrsfast
This step uses code from Peter's MPI RD mapping pipeline and runs outside snakemake, but automatically picks the correct files from the previous steps. These files are your repeat and tandem repeat-masked contig, a list of contig lengths (created in the contig prep steps), and a tab-delimited list with sample names and bam paths for mapping (specified in ''config.json'' file, 236 hgdp samples by default).

To queue the mapping jobs, run:
```
snakemake -s contig_setup_custom.snake --configfile config.json setup_rd_mapping
```

This will qsub an mpi_READER, mpi_RUNNER, and MPI_WRANGLER job for each sample in ''bam_list''. These jobs are submitted in a hold state, so nothing is running yet. Run this command to split the samples and begin running three at a time:
```
python /net/eichler/vol2/eee_shared/pipelines/MPI_mrsfast_mapping/qrls_jid_triplets.py -n 3 --fn_triplets job_id_triplets.txt | bash
```

Depending on the size of your custom contig and the number of samples being mapped, this step will take days to weeks, so be patient.

TIP:
If you need to delete these jobs, run:

```
qstat -u `whoami` | grep "mpi_" | awk '{print $1}' | xargs qdel
```

This will also delete any other jobs with ''mpi_'' in their name.

##Getting WSSD combined corrected files
*This section is still being developed.*

