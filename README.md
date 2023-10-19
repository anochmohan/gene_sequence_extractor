# gene_sequence_extractor

Task:

Takes the following inputs as command line input:
1. The path to a BLAST output 
2. The path to a BED file 
3. The path to an assembly in FASTA format
4. The path to an output file that your script will write

Performs the following operations:
1. Processes the BLAST output to keep only hits with >30% identity and 90% length
2. Identify BED features (i.e., genes) that have a BLAST hit entirely within the boundaries of the feature start and end 
3. Extract the sequence of identified homologous genes from the assembly sequence
4. If the gene is encoded on the - strand (indicated in the BED file), reverse complement the sequence
5. Write the sequences of the homologous genes to the specified output file (specified using command line input) in FASTA format (gene name as header).

If you correctly check that BLAST hits are on the same sequence as BED features and within the boundaries of the feature, you should get 34 homologs for the *Vibrio cholerae* assembly.

If you correctly extract gene sequences, you should get the below sequence for the *V. cholerae* *glnL*

```
>glnL
GTGAGTGCAGAATTAAGCCAAACCATCATTAATAATCAGGTCACATCAGTGCTCATTTTGGACGAGTCACTGATGATTCGCTACGCCAACCCTGCCGCTGAACAGCTGTTTTCACAAAGTGCTAAACGCTTGATGCATCAAAGCTTAAATCATTTAGTGCAACACTCCTCTCTCGATTTACAACTGCTCACGCAGCCACTCCAGAGCGGACAAAGCATTACTGACAGCGATGTCACCTTGGTGATCGATAGCAAACCCTTAATGCTCGAAGTCACCGTCAGCCCGATTTCTTGGCACAAAGAGCTGCTGTTACTGGCCGAAATGCGCACGATTGGTCAACAACGCCGGCTAACCCAAGAACTCAATCAACACGCTCAGCAACAAGCGGCTAAGTTATTGGTCAGAGGCTTGGCTCATGAAATCAAAAATCCTTTGGGTGGTTTAAGAGGTGCGGCCCAGCTCTTAGAGCGTATGCTTCCCGATCCGGCCCTGATGGAATATACCCAAATCATCATCGAACAGGCAGATCGCTTGCGGGGATTGGTTGATCGCTTACTCGGCCCGCAACGTCCGGGGGAGAAAAAATGGGAAAACCTTCACCTGATTTTGGAGAAGGTGCGTCAGTTGGTCGAGCTAGAAGCGGGCGCGAATTTGGTCTTTGAGCGCGATTATGACCCAAGTCTGCCGAATATTTTGATGGACACTGATCAAATCGAACAAGCCTTACTGAACATTGTCAGTAATGCGGCGCAAATTTTGACTAACCAAACGCACGGCGTGATCACCTTGCGCACCAGAACAGTGCATCAAGCCAATATCCATGGTCAACGTCATAAGCTCGTCGCCAGCATCGAGATTATCGATAACGGCCCCGGCATCCCTCCTGAGCTGCAAGATACGCTGTTTTATCCCATGGTGAGTGGCCGCGAAGGAGGCACTGGCTTGGGGTTATCCATTTCACAAAACCTGATCGATCAACATCAGGGAAAAATAGAGGTGCAAAGCTGGCCAGGACGCACCGTGTTTACCATTTATTTGCCAATTTTGAATTGCTGT
```

**Note** All processing must be done in Python except for running BLAST. You must run BLAST using a command like that below (with filepaths pointing to wherever the files are on your system). Don't use `-task tblastn-fast`.

```
tblastn -query data/HK_domain.faa -subject data/Vibrio_cholerae_N16961.fna -outfmt '6 std qlen' > Vc_blastout.txt
```

Usage of your script should be 

`./<script name>.py <blast file> <bed file> <assembly file> <output file>`
