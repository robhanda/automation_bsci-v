
#these details are for memory leak macros-
# please enter type of bsc as Flexi or mcbsc
bsc_type = "Flexi"
bsc_ip = "10.43.85.108"
pcu_ip="180.144.58.109"
bcsu_id = "0"
pcu_id = "0004"
pcum_id = "4"
no_of_bcf = 2
bts_per_bcf= 2
pidm_ip = "10.0.1.24"



# details to be entered for copying macro 

filePathegprs = "/home/Automation/gteconfigfiles/egprs.conf"
filePathgprs = "/home/Automation/gteconfigfiles/gprs.conf"
filePathegprstest = "/home/Automation/gtestatemachines/egprs_test.tcl"
filePathgprstest = "/home/Automation/gtestatemachines/gprs_test.tcl"
#filePathelgmsmacro = "/home/gemu/elgmsmacro.mac"
filePathelgmsmacro = "/home/Automation/gteconfigfiles/pet_gprs_data.mac"

serverPathconf = "/root/gte/profile"
serverPath = "/home/gemu/bcf/system/macros"
serverPath1 = "/home/gemu/bcf_1/system/macros"
serverPath2 = "/home/gemu/bcf_2/system/macros"
serverPath3 = "/home/gemu/bcf_3/system/macros"




#these details are for pqdsp loadanalysis macro that will fetch details from stat manager-

stat_ip="10.253.192.52"
destination_path= "/root"
number_of_pqdsp="7"
#bsc_ip="10.53.153.28"
vnc_instance=1






'''

# this machine has ip of stat manager and destination path where while needs to be copied
# password less ssh/scp should be enabled in machine where we are going to copy this file
# otherwise make ssh/scp password less by generator tool script ./makesshconfig.tcl managementip

enter the value of pq+dsp

mcbsc pq+dsp=9+23=32
pcu2d-1+7=8
pcu2e=1+6=7


//command to check dsp -
pcu2d and pcu2e- ddspinfo
mcbsc- top dsp

//command to check pq2-
pcu2d and pcu2e- 1
mcbsc-top pq2





'''























