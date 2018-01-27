./confgenerator.tcl pabise 1 1 20 10.253.192.54 2 /root/generator_tools/example/confgenerator/pabis_4bts_g_Eth.conf /root/BCF_CONFIGURATION/ struct_2g.db 1

# creating msinfo.dat
./msvlrinfogen.tcl mscall 1 1 2 /root/generator_tools/example/msvlrinfogen/cs_ps1.conf /root/BCF_CONFIGURATION/


./gemusync.tcl pabise 1 20 @REF[/root/generator_tools/managementip]@ 2 /root/gprs3gemulator-6.17.8-corr1 /home/gemu/bcf

#copying packet abis related binaries to all vm's
./gemusync.tcl pabise 1 20 @REF[/root/generator_tools/managementip]@ 2 /root/gprs3gemulator-6.17.8-corr1 /home/gemu/bcf

# ms struct file struc2g_ms for all bcf
./confgenerator.tcl ms 1 1 20  10.253.192.54 2 /root/generator_tools/example/confgenerator/ms_4bts.conf /root/BCF_CONFIGURATION_GPRS/ struct_2g_ms.db
./confgenerator.tcl ms 1 1 20  10.253.192.54 2 /root/generator_tools/example/confgenerator/ms_5bts.conf /root/BCF_CONFIGURATION_EGPRS/ struct_2g_ms.db
./confgenerator.tcl ms 1 1 20  10.253.192.54 2 /root/generator_tools/example/confgenerator/ms_6bts.conf /root/BCF_CONFIGURATION_PEO/ struct_2g_ms.db
./confgenerator.tcl ms 1 1 20  10.253.192.54 2 /root/generator_tools/example/confgenerator/ms_7bts.conf /root/BCF_CONFIGURATION_ECGSM/ struct_2g_ms.db

# copying ms related binaries bcf,bcf_1
./gemusync.tcl ms 1 20  @REF[/root/generator_tools/managementip]@ 2 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/bcf/
# will copy ms process related binaries from gemu load
./gemusync.tcl ms 1 1  @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/GPRS
./gemusync.tcl ms 1 1  @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/EGPRS
./gemusync.tcl ms 1 1  @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/PEO
./gemusync.tcl ms 1 1  @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/ECGSM


# copy  pabise binary  to different folders
./gemusync.tcl pabise 1 10 @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/GPRS
./gemusync.tcl pabise 1 10 @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/EGPRS
./gemusync.tcl pabise 1 10 @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/PEO
./gemusync.tcl pabise 1 10 @REF[/root/generator_tools/managementip]@ 1 /root/gprs3gemulator-6.17.8-corr1/ /home/gemu/ECGSM

# will copy above generated cofig(struct_2g_ms) to all folders with iniparser
./confsync.tcl bcf 1 1 @REF[/root/generator_tools/managementip]@ 1 /root/BCF_CONFIGURATION_GPRS/ /home/gemu/GPRS
./confsync.tcl bcf 1 1 @REF[/root/generator_tools/managementip]@ 1 /root/BCF_CONFIGURATION_EGPRS/ /home/gemu/EGPRS
./confsync.tcl bcf 1 1 @REF[/root/generator_tools/managementip]@ 1 /root/BCF_CONFIGURATION_PEO/ /home/gemu/PEO
./confsync.tcl bcf 1 1 @REF[/root/generator_tools/managementip]@ 1 /root/BCF_CONFIGURATION_ECGSM/ /home/gemu/ECGSM

# copy main struct file containing BTS realted parameters to aal vm's
./confsync.tcl bcf 1 20 @REF[/root/generator_tools/managementip]@ 2 /root/BCF_CONFIGURATION/ /home/gemu/bcf











