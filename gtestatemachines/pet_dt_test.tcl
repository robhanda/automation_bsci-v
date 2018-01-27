#!/usr/bin/expect

# test macro for procedure:
# attach and pdp all,
# data transfer
# detach all

proc ElgTestMacro { } {
    global gElg
    global gDie
    global gVar
    global gErrorCounter
    global gEnable
    global gErrorSet
    global gExpireTime

    # initial state
    set pState DISABLERAU
    # init while loop
    set pRunning 1
    # init errorset
    set gErrorSet 0

    # game loop
    while { $pRunning } {
	update
	#WriteLog $pState
	switch $pState {
	    "DISABLERAU" {
		# disable rau
		Setmsapp99Variable rau_disabled 1
		set pState DT
	    }
	    "DT" {
		# Figure 23.1 A
		set pExitCode [ WaitProcedureEnd DT $gElg(ATTACHTIMER) $gElg(MSAMOUNT) $gElg(MSLOWLIMIT) ]
		if { $pExitCode == 1 } { 
		    # if required attach amount was not reached
		    set pState DETACH 
		    incr gErrorCounter
		} elseif { $pExitCode == 2 } {
		    # elg was disabled
		    set pState DETACH 
		} elseif { $pExitCode == -1 } {
		    # eof was detected
		    set pRunning 0
		} else { 
		    # all ok
		    set pState SURVEILANCE
		    RunningStateChange $pState
		}
		# if die command received
		if {$gDie==1} { set pState DETACH }
		# calculate next step end time
		set pEndTime [ GetEndTime $gElg(TIMER1) ]
	    }
	    "SURVEILANCE" {
		set gErrorCounter 0
		# Figure 23.1 B
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
		# Figure 23.1 C
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
		# Figure 23.1 D
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
	after 1000
    }

    RunningStateChange END
    
    # Figure 23.1 E
    if { $gErrorCounter >= $gVar(ERRORLIMIT) } {
	# Figure 23.1 F
	# return 1 if max error amount is reached
	set gErrorCounter 0
	return 1
    } else {
	# normal run return 0
	return 0
    }
}
