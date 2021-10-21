/** @example notification.c
 *  This example shows how to send a notification from inside the
 *  agent.  In this case we do something really boring to decide
 *  whether to send a notification or not: we simply sleep for 30
 *  seconds and send it, then we sleep for 30 more and send it again.
 *  We do this through the snmp_alarm mechanisms (which are safe to
 *  use within the agent.  Don't use the system alarm() call, it won't
 *  work properly).  Normally, you would probably want to do something
 *  to test whether or not to send an alarm, based on the type of mib
 *  module you were creating.
 *
 *  When this module is compiled into the agent (run configure with
 *  --with-mib-modules="examples/notification") then it should send
 *  out traps, which when received by the snmptrapd demon will look
 *  roughly like:
 *
 *  2002-05-08 08:57:05 localhost.localdomain [udp:127.0.0.1:32865]:
 *      sysUpTimeInstance = Timeticks: (3803) 0:00:38.03        snmpTrapOID.0 = OID: netSnmpExampleNotification
 *
 */

/*
 * start be including the appropriate header files 
 */
#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>
#include <net-snmp/agent/net-snmp-agent-includes.h>

/*
 * contains prototypes 
 */
#include "TestTraps.h"

#include <Python.h>
#include <stdarg.h>

unsigned char buf[1024];

/* for acceptable `arg_format' `ret_val_format', see https://docs.python.org/2.7/c-api/arg.html */
int int_py_caller(char *python_module_name, char *python_func_name, char *arg_format, char *ret_val_format, ...)
{
  PyObject *python_module_object    = NULL;
  PyObject *python_arg_object   = NULL;
  PyObject *python_func_object    = NULL;
  PyObject *python_return_val_object  = NULL;

  va_list vl; /* this is used to parse the arguments in the `...' part. see stdarg(3) */

  Py_Initialize();

  /* these two lines are required, if any custom module under the current working dirctory is to be loaded */
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append('.')");

  python_module_object = PyImport_ImportModule(python_module_name); 
  if (!python_module_object) {
    printf("Error: cannot import module.\n");
    // return 0; // TODO:
  }

  python_func_object = PyObject_GetAttrString(python_module_object, python_func_name);
  if (!python_func_object) {
    printf("Error: cannot import function.\n");
    // return 0; // TODO:
  }

  /* start parsing arguments */
  va_start(vl, ret_val_format);
  /* construct arguments for the python function using the arguments passed to this C function */
  python_arg_object = Py_VaBuildValue(arg_format, vl);
  if (!python_arg_object) {
    printf("Error: cannot construct arguments.\n");
    // return 0; // TODO:
  }
  /* finish parsing arguments */
  va_end(vl);

  // PyObject_Print(python_arg_object, stdout, 0/*Py_PRINT_RAW*/); /* the 3rd arg controls either using `str()' or `repr()' */
  // printf("\n");


  /* `python_arg_object' should be a tuple */
  python_return_val_object = PyEval_CallObject(python_func_object, python_arg_object);
  if (!python_return_val_object) {
    printf("Error: function not called successfully.\n");
    // return 0; // TODO:
  }

  // TODO: another function? use tuple or not? what if multiple return value?
  // after experiemnt, PyArg_Parse can't use tuple
  if (!PyArg_Parse(python_return_val_object, ret_val_format, buf)) {
    printf("Error: cannot parse return value.\n");
    // return 0; // TODO:
  }

  // TODO: unified way of handling types
  printf("%d\n", *((int *) buf));

  Py_DECREF(python_module_object);
  Py_DECREF(python_func_object);
  Py_DECREF(python_arg_object);
  Py_DECREF(python_return_val_object);

  return *((int *) buf);
}

/*
 * contains prototypes 
 */
#include "TestTraps.h"
static u_long count = 0;
int cputrap_clientreg = 0; 
int cpu = 90;  
int value = 0;
/*
 * our initialization routine
 * (to get called, the function name must match init_FILENAME() 
 */
void read_cpudata_repeat(unsigned int clientreg, void *clientarg);  
void
init_TestTraps(void)
{
    DEBUGMSGTL(("example_notification",
                "initializing (setting callback alarm)\n"));
    snmp_alarm_register(10,     /* seconds */
                        SA_REPEAT,      /* repeat (every 30 seconds). */
                        read_cpudata_repeat,      /* our callback */
                        NULL    /* no callback data needed */
        );
}

/** here we send a SNMP v2 trap (which can be sent through snmpv3 and
 *  snmpv1 as well) and send it out.
 *
 *     The various "send_trap()" calls allow you to specify traps in different
 *  formats.  And the various "trapsink" directives allow you to specify
 *  destinations to receive different formats.
 *  But *all* traps are sent to *all* destinations, regardless of how they
 *  were specified.
 *  
 *  
 *  I.e. it's
 * @verbatim
 *                                           ___  trapsink
 *                                          /
 *      send_easy_trap \___  [  Trap      ] ____  trap2sink
 *                      ___  [ Generator  ]
 *      send_v2trap    /     [            ] ----- informsink
 *                                          \____
 *                                                trapsess
 *  
 *  *Not*
 *       send_easy_trap  ------------------->  trapsink
 *       send_v2trap     ------------------->  trap2sink
 *       ????            ------------------->  informsink
 *       ????            ------------------->  trapsess
 * @endverbatim
 */
void read_cpudata_repeat(unsigned int clientreg, void *clientarg)  
{  
  value = int_py_caller("ieeeP1451CommandTrap", "get_int", "(i)", "i", 999);
  judge_send_trap(value); 
}  


void judge_send_trap(int value)  
{  
 
  // if(count > 10)
  // {
  //   cputrap_clientreg = 1;
  // } 
  if(value == 1)  
  {  
    if(cputrap_clientreg == 0){  
      send_cpuRatioHigh_trap();  
      cputrap_clientreg = snmp_alarm_register(5,SA_REPEAT,send_cpuRatioHigh_trap,NULL);  
      
    }  
  }  
  else  
  {  
      snmp_alarm_unregister(cputrap_clientreg);  
      cputrap_clientreg = 0;  
  }  
}  

int
send_cpuRatioHigh_trap(void)
{
    /*
     * define the OID for the notification we're going to send
     * NET-SNMP-EXAMPLES-MIB::netSnmpExampleHeartbeatNotification 
     */

    oid             notification_oid[] =
        { 1, 3, 6, 1, 4, 1, 8072, 2, 3, 0, 1 };
    size_t          notification_oid_len = OID_LENGTH(notification_oid);
    

    /*
     * In the notification, we have to assign our notification OID to
     * the snmpTrapOID.0 object. Here is it's definition. 
     */
    oid             objid_snmptrap[] = { 1, 3, 6, 1, 6, 3, 1, 1, 4, 1, 0 };
    size_t          objid_snmptrap_len = OID_LENGTH(objid_snmptrap);

    /*
     * define the OIDs for the varbinds we're going to include
     *  with the notification -
     * NET-SNMP-EXAMPLES-MIB::netSnmpExampleHeartbeatRate  and
     * NET-SNMP-EXAMPLES-MIB::netSnmpExampleHeartbeatName 
     */
    oid      hbeat_rate_oid[]   = { 1, 3, 6, 1, 4, 1, 8072, 2, 3, 2, 1, 0 };
    size_t   hbeat_rate_oid_len = OID_LENGTH(hbeat_rate_oid);
    oid      hbeat_name_oid[]   = { 1, 3, 6, 1, 4, 1, 8072, 2, 3, 2, 2, 0 };
    size_t   hbeat_name_oid_len = OID_LENGTH(hbeat_name_oid);

    /*
     * here is where we store the variables to be sent in the trap 
     */
    netsnmp_variable_list *notification_vars = NULL;
    const char *heartbeat_name = "The buzzer of TIM is ringing";
#ifdef  RANDOM_HEARTBEAT
    int  heartbeat_rate = rand() % 60;
#else
    int  heartbeat_rate = 1;
#endif

    netsnmp_pdu *pdu;
    int status = 0;
    pdu = snmp_pdu_create(SNMP_MSG_TRAP2); //SNMP_MSG_TRAP
    status = create_trap_session("127.0.0.1", SNMP_TRAP_PORT, "public", SNMP_VERSION_2c, SNMP_MSG_TRAP2);
    // status = create_trap_session("47.103.50.213", 162, "public", SNMP_VERSION_2c, SNMP_MSG_TRAP2);
    ++count;
    int flag = 1;
    //cpu利用率大于85%时，添加到trap列表中
    if ( cpu > 80)
    {
      flag = 1;
      status = snmp_add_var(pdu, hbeat_name_oid, OID_LENGTH(hbeat_name_oid), 's', "temperature_is_too_high");
    }
    else
    {
      snmp_free_pdu(pdu);
    }
    if(1)
    {
      send_trap_vars(1, 0, pdu->variables);
    }
    //释放资源
    snmpd_free_trapsinks();
    snmp_free_pdu(pdu);

    // DEBUGMSGTL(("example_notification", "defining the trap\n"));

    // /*
    //  * add in the trap definition object 
    //  */
    // snmp_varlist_add_variable(&notification_vars,
    //                           /*
    //                            * the snmpTrapOID.0 variable 
    //                            */
    //                           objid_snmptrap, objid_snmptrap_len,
    //                           /*
    //                            * value type is an OID 
    //                            */
    //                           ASN_OBJECT_ID,
    //                           /*
    //                            * value contents is our notification OID 
    //                            */
    //                           (u_char *) notification_oid,
    //                           /*
    //                            * size in bytes = oid length * sizeof(oid) 
    //                            */
    //                           notification_oid_len * sizeof(oid));

    // /*
    //  * add in the additional objects defined as part of the trap
    //  */

    // snmp_varlist_add_variable(&notification_vars,
    //                            hbeat_rate_oid, hbeat_rate_oid_len,
    //                            ASN_INTEGER,
    //                            &heartbeat_rate,
    //                               sizeof(heartbeat_rate));

    // /*
    //  * if we want to insert additional objects, we do it here 
    //  */
    // if (heartbeat_rate < 30 ) {
    //     snmp_varlist_add_variable(&notification_vars,
    //                            hbeat_name_oid, hbeat_name_oid_len,
    //                            ASN_OCTET_STR,
    //                            heartbeat_name, strlen(heartbeat_name));
    // }

    // /*
    //  * send the trap out.  This will send it to all registered
    //  * receivers (see the "SETTING UP TRAP AND/OR INFORM DESTINATIONS"
    //  * section of the snmpd.conf manual page. 
    //  */
    // ++count;
    // DEBUGMSGTL(("example_notification", "sending trap %ld\n",count));
    // send_v2trap(notification_vars);

    // /*
    //  * free the created notification variable list 
    //  */
    // DEBUGMSGTL(("example_notification", "cleaning up\n"));
    // snmp_free_varbind(notification_vars);
}
