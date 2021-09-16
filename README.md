# HPE3par-Automation

Create Volumes according to the information in HPE3parAutomation.xlsx

ID	Volume Name	Size(GB)	usr CPG	snap CPG	TPVV
1	     demo_vv1	 11	       FC_r5	FC_r5	    TRUE
2	     demo_vv2	 12	       FC_r6	none	    FALSE
3	     demo_vv3	 13	       FC_r5	none	    TRUE
4	     demo_vv4	 14	       FC_r5	None	    TRUE
5	     demo_vv5	 15	       FC_r5	FC_r5	    TRUE

The script is verified in python 3.8,  HPE 3par OS 3.2.2 MU6, 3.3.1MU2+

python HPE3par-createvv.py will create volumes that customized in the table



