# import section
from pysnmp.hlapi import *
from datetime import datetime

# var section

# snmp
community_string = 'public'
port_snmp = 161

# log
filename_log = 'snmp_logs.log'  # для лог файла
log_level = 'debug'

domain = ''


# function section
def snmp_getcmd(community, ip, port, OID):

    # type class 'generator' errorIndication, errorStatus, errorIndex,
    # result[3] - список метод get получаем результат обращения к
    # устойстройству по SNMP с указаным OID
    return (getCmd(SnmpEngine(),
                   CommunityData(community),
                   UdpTransportTarget((ip, port)),
                   ContextData(),
                   ObjectType(ObjectIdentity(OID))))


def snmp_get_next(community, ip, port, OID, file):

    # Метод обрабатывает class generator от def snmp_get
    # обрабатываем errors, выдаём тип class 'pysnmp.smi.rfc1902.ObjectType'
    # с OID (в name) и значением  (в val) получаем одно скалярное значение
    error_indication, error_status, error_index, var_binds = \
                   next(snmp_getcmd(community, ip, port, OID))

    if errors(error_indication, error_status, error_index, ip, file):

        for name, val in var_binds:
            return val.prettyPrint(), True

    else:

        file.write(datetime.strftime(datetime.now(),
                   "%Y.%m.%d %H:%M:%S") +
                   ' : Error snmp_get_next ip = ' +
                   ip + ' OID = ' + OID + '\n')

        return 'Error', False


def errors(errorIndication, errorStatus, errorIndex, ip, file):

    #  обработка ошибок в случае ошибок возвращаем False и пишем в файл file

    if errorIndication:
        print()
        print(errorIndication, 'IP Address:', ip)
        file.write(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") +
                   ' : ' + str(errorIndication) + ' = ip address = ' + ip + '\n')
        return False

    elif errorStatus:

        print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' : ' + '%s at %s' % (
            errorStatus.prettyPrint(), errorIndex))

        file.write(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' : ' + '%s at %s' % (
            errorStatus.prettyPrint(), errorIndex))

        return False

    else:
        return True


def snmp_get_data(list_of_hosts, filed):

    for host in list_of_hosts:

        OID_sysName = '1.3.6.1.2.1.1.5.0'  # From SNMPv2-MIB hostname/sysname

        # Получаем sysname hostname+domainname, флаг ошибки.
        sysname, flag_snmp_get = (snmp_get_next(community_string, host.ip_address,
                                                port_snmp, OID_sysName, filed))

        if flag_snmp_get:

            # Всё хорошо, хост ответил по SNMP.

            OID_sysDescr = '1.3.6.1.2.1.1.1.0'  # From SNMPv2-MIB sysDescr

            # Получаем sysDescr, флаг ошибки.
            sysDescr, flag_snmp_get_sysdescr = (snmp_get_next(community_string, host.ip_address,
                                                     port_snmp, OID_sysDescr, filed))

            if sysname == 'No Such Object currently exists at this OID':
                # а community неверный.надо пропускать хост, иначе словим traceback.
                # Причём никак не поймаешь, что проблема в community, поэтому
                # всегда надо запрашивать hostname, который отдают все устройства.
                print('ERROR community', sysname, ' ', host.ip_address)
                filed.write(datetime.strftime(datetime.now(),
                            "%Y.%m.%d %H:%M:%S") + ' : ' +
                            'ERROR community sysname = ' +
                            sysname + ' ip = ' + host.ip_address
                            + '\n')
            else:

                if log_level == 'debug':
                    filed.write(datetime.strftime(datetime.now(),
                                "%Y.%m.%d %H:%M:%S") + ' : ' +
                                ' sysname ' + sysname + ' type '
                                + str(type(sysname)) +
                                ' len ' + str(len(sysname))
                                + ' ip ' + host.ip_address + '\n')

                if len(sysname) < 3:
                    sysname = 'Hostname unknown'

                    if log_level == 'debug' or log_level == 'normal':
                        filed.write(datetime.strftime(datetime.now(),
                                    "%Y.%m.%d %H:%M:%S") + ' : ' +
                                    'Error sysname 3 = ' + sysname +
                                    ' ip = ' + host.ip_address + '\n')

                if sysname.find(domain) == -1:

                    # Что-то отдало hostname без домена, например Huawei или Catos.
                    sysname = sysname + '.' + domain

                    if log_level == 'debug' or log_level == 'normal':
                        filed.write("check domain: " + sysname + " "
                                    + host.ip_address + " " + "\n")

                # Всё хорошо, хост ответил по SNMP.
                if sysDescr == 'No Such Object currently exists at this OID':
                    # а community неверный.надо пропускать хост, иначе словим traceback.
                    # Причём никак не поймаешь, что проблема в community, поэтому
                    # всегда надо запрашивать hostname, который отдают все устройства.
                    print('ERROR community', sysDescr, ' ', host.ip_address)
                    filed.write(datetime.strftime(datetime.now(),
                                "%Y.%m.%d %H:%M:%S") + ' : ' +
                                'ERROR community sysDescr = ' +
                                sysDescr + ' ip = ' + host.ip_address
                                + '\n')
                else:

                    if log_level == 'debug':
                        filed.write(datetime.strftime(datetime.now(),
                                    "%Y.%m.%d %H:%M:%S") + ' : ' +
                                    ' sysDescr ' + sysDescr + ' type '
                                    + str(type(sysDescr)) +
                                    ' len ' + str(len(sysDescr))
                                    + ' ip ' + host.ip_address + '\n')

                    if len(sysDescr) < 3:
                        sysDescr = 'System Description unknown'

                        if log_level == 'debug' or log_level == 'normal':
                            filed.write(datetime.strftime(datetime.now(),
                                        "%Y.%m.%d %H:%M:%S") + ' : ' +
                                        'Error sysDescr 3 = ' + sysDescr +
                                        ' ip = ' + host.ip_address + '\n')

                print("\nHost IP Address:", host.ip_address)
                print("Hostname = %s" % str(sysname))
                print("System Description:\n%s" % str(sysDescr))
                host.set_hostname(str(sysname))
                host.set_sysdecr(str(sysDescr))


def snmp_scan(list_of_hosts):

    print("Okay. Starting SNMP scanning...")

    # Открываем лог файл
    filed = open(filename_log, 'w')

    # Записываем текущее время
    filed.write(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + '\n')

    # Запускаем цикл по перебору IP адресов.
    snmp_get_data(list_of_hosts, filed)

    filed.close()


