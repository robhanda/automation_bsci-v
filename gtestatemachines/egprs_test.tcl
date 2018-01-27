#!/usr/bin/expect

# test macro for procedure:
# attach all,
# pdp all,
# data transfer
# detach all

proc ElgTestMacro { } {
    global gElg
    global gDie
    global gErrorCounter
    global gErrorLimit
    global gEnable
    global gErrorSet
    global gExpireTime

    # initial state
    set pState ATTACH
    # init while loop
    set pRunning 1
    # init errorset
    set gErrorSet 0

    # game loop
    while { $pRunning } {
	switch $pState {
	    "ATTACH" {
		# Figure 23.2 A
		set pExitCode [ WaitProcedureEnd ATTACH $gElg(ATTACHTIMER) $gElg(MSAMOUNT) $gElg(MSLOWLIMIT) ]
		if { $pExitCode == 1 } { 
		    # if required attach amount was not reached
		    set pState DETACH 
		} elseif { $pExitCode == 2 } {
		    # elg was disabled
		    set pState DETACH 
		} elseif { $pExitCode == -1 } {
		    # eof was detected
		    set pRunning 0
		} else { 
		    # all ok
		    set pState PDP
		}
		# if die command received
		if {$gDie==1} { set pState DETACH }
	    }
	    "PDP" {
		# Figure 23.2 B
		set pExitCode [ WaitProcedureEnd PDP $gElg(PDPTIMER) $gElg(MSAMOUNT) $gElg(MSLOWLIMIT) ]
		if { $pExitCode == 1 } { 
		    # if required attach amount was not reached
		    set pState DETACH 
		} elseif { $pExitCode == 2 } {
		    # elg was disabled
		    set pState DETACH  
		} elseif { $pExitCode == -1 } {
		    # eof was detected
		    set pRunning 0
		} else { 
		    # all ok
		    set pState SURVEILANCE
		}
		# calculate next step end time
		set pEndTime [ GetEndTime $gElg(TIMER1) ]
		# if die command received
		if {$gDie==1} { set pState DETACH }
	    }
	    "SURVEILANCE" {
		# Figure 23.2 C
		set pExitCode [ MonitorData $pEndTime $gElg(ULLIMIT) $gElg(DLLIMIT) ]
		if { $pExitCode == 1 } {
		    # if UL or DL TP was lower than required
		    set pState DETACH 
		} elseif { $pExitCode == 2 } {
		    # elg was disabled
		    set pState DETACH 
		} elseif { $pExitCode == -1 } {
		    # eof was detected
		    set pRunning 0
		} else {
		    # all ok
		    set pState DETACH 
		}
	    }
	    "DETACH" {
		# Figure 23.4 D
		set pExitCode [ WaitProcedureEnd DETACH $gElg(DETACHTIMER) 0 0 ]
		if { $pExitCode == 1 } {
		    # i think there can't be situtation when requred detach 
		    # amount is not reached 0, but just in case
		    set pState WAIT
		} elseif { $pExitCode == 2 } {
		    # elg was disabled
		    set pState WAIT 
		} elseif { $pExitCode == -1 } {
		    # eof was detected
		    set pRunning 0
		} else {
		    # all ok
		    set pState WAIT
		}
	    }
	    "WAIT" {
		# Figure 23.2 E
		if { [ IdleLoop WAIT 10 ] == 0 } {
		    # give PCUMS time to clear memory
		    # exit while loop
		    set pRunning 0
		}
	    }
	}
	# time based profile change
	if { $gExpireTime != "null" } {
	    # profile expirations time is set 
	    if { $gExpireTime <= [ clock seconds ] } {
		# is profile expired, detach ms(s)
		WriteLog "Profile Expired"
		set pState DETACH
	    }
	}
	update
    }

    RunningStateChange END
    
    # Figure 23.2 F
    if { $gErrorCounter >= $gErrorLimit } {
	# Figure 23.s G
	# return 1 if max error amount is reached
	set gErrorCounter 0
	return 1
    } else {
	# normal run return 0
	return 0
    }
}
