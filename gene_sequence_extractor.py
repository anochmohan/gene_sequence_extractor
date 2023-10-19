#!/usr/bin/env python3
import sys

blastfile = sys.argv[1]
bedfile = sys.argv[2]
fastafile = sys.argv[3]
outputfile = sys.argv[4]

# read blast file
hits = []
with open(blastfile) as fin:
    for line in fin: # .readlines() is the default iter method for the open file class
        
        # unpack and convert types of desired columns. This is ugly. We'll revisit later...
        _, sid, pcnt, matchlen, _, _, _, _, sstart, send, _, _, qlen = line.split()
        pcnt = float(pcnt)
        matchlen = int(matchlen)
        sstart = int(sstart)
        send = int(send)
        qlen = int(qlen)
    
        # Keep hits that could be homologs
        if pcnt > 30 and matchlen > 0.9*qlen:
            # We could store matches as a list or tuple.
            # We won't want to modify the elements so a tuple is "safer" in that we then can't modify it by mistake
            hits.append((sid, sstart, send))

# Now read the bed file
feats = []
with open(bedfile) as fin:
    for line in fin:
        bed_sid, bed_start, bed_end, gene, dot, direction = line.split() # an asterisk before a variable name when unpacking makes that variable store remaining elements
        bed_start = int(bed_start)
        bed_end = int(bed_end)
        
        feats.append((bed_sid, bed_start, bed_end, gene, direction))

# Now we have our two datasets read in, we can loop over them to find matches
homologs = []
for blast_sid, blast_sstart, blast_send in hits: # unpack our blast data
    for bed_sid, bed_start, bed_end, gene, direction in feats:
        # Don't bother checking the rest if the sid doens't match
        if blast_sid != bed_sid:
            continue
        
        # Once we are dealing with features at higher index locations than our hit, go to the next hit (break loop over feats)
        if blast_sstart <= bed_start or blast_send <= bed_start:
            break
        
        # Otherwise, check if the hit is inside the feature
        if (blast_sstart > bed_start
            and blast_sstart <= bed_end
            and blast_send > bed_start
            and blast_send <= bed_end
        ):
            homologs.append((bed_sid, bed_start, bed_end, gene, direction))
            break # Each BLAST hit will only be in one feature so move to next hit once you've found it

# Get the unique homologs using a set()
unique_homologs = set(homologs)

# Part 3,4,5

# Empty dict and list
fasta_dict={}
sequence_list = []

with open (fastafile) as fin:   # open previously made fasta file
    for i in fin:   # for line in fasta file
        if i[0] == ">": # if first charecter of line i has ">"
            if sequence_list != []: # if sequence list is empty (this will not be empty later on)
                value = "".join(sequence_list)  # add the string of nucleotides into an empty string and store in value
                fasta_dict[chromosome]=value    # enter chromosome and value into dict
                sequence_list = []              # clear out the sequence list
            chromosome=i[1:].split()[0]         # save chromosome key
        else:
            sequence_list.append(i.strip())
    fasta_dict[chromosome]=value                # enter chromosome and value into dict finally


with open(outputfile, "w") as fout:
    new_counter=0   # I use this instead of chrm below bcuz chrm is string and I need to index unique_homologs
    for chrm, start, end, gen, sym in unique_homologs:
        if sym == "+":  # if gene on 5' to 3' strand
            fout.write(">" + gen + "\n") # print gene name
            fout.write(fasta_dict[list(unique_homologs)[new_counter][0]][start-1:end] + "\n")  # print string of nucleotide; but it is spliced using start and end, thus outputing just the nucleotides that make up the gene; -1 cuz of 0 indexing issues
            new_counter+=1  # go to the next chromosome
        else:
            fout.write(">" + gen + "\n") # if gene on 3' to 5' strand
            string = fasta_dict[list(unique_homologs)[new_counter][0]][start-1:end]   # string of nucleotide; but it is spliced using start and end, thus outputing just the nucleotides that make up the gene
            new_string = ""
            for j in range(0, len(string)): # if gene is encoded in the negative strand, reverse compliment the sequence
                if string[j] == "A":
                    new_string+="T"
                elif string[j] == "T":
                    new_string+="A"
                elif string[j] == "G":
                    new_string+="C"
                else:
                    new_string+="G"
            fout.write(new_string[::-1] + "\n")    # print the reverse complimented spliced nucleotides
            new_counter+=1  # go to the next chromosome
