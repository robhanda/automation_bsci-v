
import ConfigParser,os,sys,time

def findalivemachines(ip,num_of_VM,num_of_Ips_PerVM):
	global hostname	
	hostname=[]
	num_of_VM=num_of_VM+1
	ip_parts = ip.split(".")
	ip_parts = [int(part) for part in ip_parts]
	first, second, third, fourth = ip_parts

	#print first, second, third, fourth


	for i in range(1,num_of_VM):

    		result = os.system("ping -c 2 " +str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)+" > /dev/null 2>&1")

    		#fourth= fourth +4

    		if result == 0:
        		#print("ip %s is pinging" %i)
			comp_ip=str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)
			#print comp_ip
		        hostname.append(comp_ip)


   	 	else:
        		print("ip %s is not pinging" %i)

		fourth=fourth+num_of_Ips_PerVM
	return hostname




if __name__ == "__main__":
	gemuConfigfile = ConfigParser.ConfigParser()
	gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
	num_of_VM=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_gemu_machines"))
        gemu_StartIp=gemuConfigfile.get("Test_Environment_GEMU","gemu_machine_start_ip")
	num_of_Ips_PerVM=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_bcf_per_machine"))
	aliveMachines=findalivemachines(gemu_StartIp,num_of_VM,num_of_Ips_PerVM)
	print aliveMachines
	









