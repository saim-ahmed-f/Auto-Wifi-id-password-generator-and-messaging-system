# UserImport
#
# Takes basic User definitions from a CSV file and posts
# them to an XG Firewall using the XML API

import xml.etree.ElementTree as ET
import argparse
import requests
import sys
import configparser
import csv



serial = 0

UserAPIAddResults = {
    "200": (True, "User registered successfully"),
    "500": (False, "User couldn't be registered"),
    "502": (False, "A user with the same name already exists"),
    "503": (False, "A user with the same L2TP/PPTP IP already exists"),
    "510": (False, "Invalid password - doesn't meet complexity requirements")
}

UserAPIUpdateResults = {
    "200": (True, "User registered successfully"),
    "500": (False, "User couldn't be updated"),
    "502": (False, "A user with the same name already exists"),
    "503": (False, "A user with the same L2TP/PPTP IP already exists"),
    "510": (False, "Invalid password - doesn't meet complexity requirements"),
    "541": (False, "There must be at least one Administrator"),
    "542": (False,
            "There must be at least one user with Administrator profile")
}


def eprint(*args, **kwargs):
    # Print to stderr instead of stdout
    print(*args, file=sys.stderr, **kwargs)


def getArguments():
    parser = argparse.ArgumentParser(
        description='Grab a list of video IDs from a YouTube playlist')

    parser.add_argument(
        '-f', '--firewall',
        help=("To call the API directly, specify a firewall hostname or IP. "
              "Without this, an XML API document will be output to stdout."),
        default=argparse.SUPPRESS)
    parser.add_argument(
        '-i', '--input', metavar="FILENAME",
        help=("Name of CSV file containing these columns:"
              " Name, Username, Password, Email Address, Group"),
        default=argparse.SUPPRESS)
    parser.add_argument(
        '-u', '--fwuser', metavar="ADMIN-USERNAME",
        help='Admin username for the XG firewall',
        default='admin')
    parser.add_argument(
        '-p', '--fwpassword', metavar="ADMIN-PASSWORD",
        help='Password for the XG user - defaults to "admin"',
        default='password')
    parser.add_argument(
        '-a', '--add',
        help=('Call API in "Add" mode - use first time only (otherwise'
              ' Update will be used)'),
        action='store_true')
    parser.add_argument(
        '-n', '--insecure',
        help="Don't validate the Firewall's HTTPS certificate",
        action='store_false')
    parser.add_argument(
        '-1', '--oneshot',
        help=("Create a single enormous XMLAPI transaction instead "
              " of multiple smaller ones. Only used when outputting "
              "to stdout "),
        action='store_true')
    parser.add_argument(
        '-x', '--useimpex',
        help=("Create an Entities.xml-style file for inclusion in an "
              " Import tarball"),
        action='store_true')

    return parser.parse_args()


def readConfig():
    # Read in the temp config file (if it exists)
    global config
    global workingPath

    config = configparser.ConfigParser()
    config.read(workingPath)


def getserial():
    # Returns an incrementing serial number. Used to reference individual
    # XMLAPI transactions.
    global serial
    serial = serial + 1
    return str(serial)


def xgAPIStartUser(username, name, password, email,status,
                   group="Open Group", usertype="User",
                   surfquota="Unlimited Internet Access",
                   accesstime="Allowed all the time",
                   datatransferpolicy="", qospolicy="", sslvpnpolicy="",
                   clientlesspolicy="", l2tp="Disable",
                   pptp="Disable", cisco="Disable",
                   quarantinedigest="Disable", macbinding="Disable",
                   loginrestriction="UserGroupNode",
                   accessschedule="All The Time", loginrestrictionapp="",
                   isencryptcert="Disable", simultaneouslogins="Enable"):
    # Returns a complete XML User record with some sane defaults which can
    # be modified later, if you want.

    userblock = ET.Element('User', transactionid=getserial())
    ET.SubElement(userblock, 'Username').text = username
    ET.SubElement(userblock, 'Name').text = name
    ET.SubElement(userblock, 'Password').text = password
    ET.SubElement(ET.SubElement(userblock, 'EmailList'),
                  'EmailID').text = email
    ET.SubElement(userblock, 'Group').text = group
    ET.SubElement(userblock, 'SurfingQuotaPolicy').text = surfquota
    ET.SubElement(userblock, 'AccessTimePolicy').text = accesstime
    ET.SubElement(userblock, 'DataTransferPolicy').text = datatransferpolicy
    ET.SubElement(userblock, 'QoSPolicy').text = qospolicy
    ET.SubElement(userblock, 'SSLVPNPolicy').text = sslvpnpolicy
    ET.SubElement(userblock, 'ClientlessPolicy').text = clientlesspolicy
    ET.SubElement(userblock, 'Status').text = status
    ET.SubElement(userblock, 'L2TP').text = l2tp
    ET.SubElement(userblock, 'PPTP').text = pptp
    ET.SubElement(userblock, 'CISCO').text = cisco
    ET.SubElement(userblock, 'QuarantineDigest').text = quarantinedigest
    ET.SubElement(userblock, 'MACBinding').text = macbinding
    ET.SubElement(userblock, 'LoginRestriction').text = loginrestriction
    ET.SubElement(
        userblock, 'ScheduleForApplianceAccess').text = accessschedule
    ET.SubElement(
        userblock, 'LoginRestrictionForAppliance').text = loginrestrictionapp
    ET.SubElement(userblock, 'IsEncryptCert').text = isencryptcert
    ET.SubElement(
        userblock, 'SimultaneousLoginsGlobal').text = simultaneouslogins

    return userblock


def xgAPILogin(fwuser, fwpassword):
    # Returns a root Login element for an XMLAPI call

    requestroot = ET.Element('Request')
    login = ET.SubElement(requestroot, 'Login')
    ET.SubElement(login, 'Username').text = fwuser
#  ET.SubElement(login, 'Password', passwordform = 'encrypt').text = fwpassword
    ET.SubElement(login, 'Password').text = fwpassword

    return requestroot


def xgImpExBegin():
    return ET.Element('Configuration', APIVersion="1702.1", IPS_CAT_VER="1")


def xgAPIPost(requestroot):
    # Posts an XMLAPI document to the firewall specified in command line -f arg
    # If there is no -f arg, it prints the document to stdout
    # Parameter 'requestroot' provides the root element of the XML document

    postdata = {
        'reqxml': ET.tostring(requestroot, 'utf-8-sig')
    }
    result = 0

    try:
        callurl = ('https://' + stuff.firewall +
                   ':443/webconsole/APIController')
        eprint("Sending XMLAPI request to %s" % callurl)

        r = requests.post(callurl, data=postdata, verify=stuff.insecure)
#        eprint(r)
#        eprint(r.text)
        result = 1
    except AttributeError:
        print(ET.tostring(requestroot, 'utf-8-sig'))
        result = 0
    return (result, r)

# Fun starts here

# Check command line
stuff = getArguments()

def run():

    try:
        eprint("Reading from file: %s" % stuff.input)
    except AttributeError:
        eprint("No filename provided. Run this command with --help for more info.")
        sys.exit()

    # If there's a firewall address set, make sure we're in oneshot mode
    try:
        eprint("Config will be posted to " + stuff.firewall)
        stuff.oneshot = True
    except AttributeError:
        eprint("No firewall set")

    if stuff.add:
        method = 'add'
    else:
        method = 'update'

    # Start building the XMLAPI Request
    if stuff.useimpex:
        fwRequestroot = xgImpExBegin()
        fwRequestSet = fwRequestroot
    else:
        fwRequestroot = xgAPILogin(stuff.fwuser, stuff.fwpassword)
        fwRequestSet = ET.SubElement(fwRequestroot, 'Set', operation=method)

    usernames = []

    # Open the csv for reading
    with open(stuff.input, encoding="utf-8-sig") as input_csv:
        csv_parser = csv.DictReader(input_csv, delimiter=',')
        count = 0
        for row in csv_parser:
            #       eprint(row)

            fwRequestSet.append(xgAPIStartUser(row["Username"], row["Name"],
                                            row["Password"],
                                            row["Email Address"],
                                            group=row["Group"]),
                                            status=row["status"])
            usernames.append(row["Username"])
            count = count + 1

        eprint("Read %d users from file %s\n" % (count, stuff.input))

    if stuff.oneshot or stuff.useimpex:
        result, r = xgAPIPost(fwRequestroot)

    if result == 1:
        resultcontent = ET.fromstring(r.text)
        for child in resultcontent:
            if child.tag == "Login":
                status = child.find('status').text
                if status == '200':
                    eprint("API login successful")
                else:
                    eprint("Login status: %s" % child.find('status').text)

            if child.tag == "User":
                Status = child.find('Status')
                eprint("Line %s (%s), Status %s" % (
                    child.attrib["transactionid"], usernames[int(
                        child.attrib["transactionid"]) - 1],
                    Status.attrib["code"]))
                try:
                    if stuff.add:
                        eprint("     %s" %
                            UserAPIAddResults[Status.attrib["code"]][1])
                    else:
                        eprint("     %s" %
                            UserAPIUpdateResults[Status.attrib["code"]][1])
                except KeyError:
                    eprint("Message: %s" % Status.text)
                    continue

            if child.tag == "Status":
                eprint("Error code %s: %s" % (child.attrib['code'], child.text))

    # Take the xml output from this program and send it to your firewall with curl,
    # for example:
    # $ curl -k https://<firewall ip>:443/webconsole/APIController -F "reqxml=<foo.xml"

    # To create an API Import file, use '-x', write the XML output to a file
    # 'Entities.xml' and create a tarball with the following (group/owner options 
    # to make it anonymous):
    # $ tar --group=a:1000 --owner=a:1000 --numeric-owner -cvf ../API-O365.tar Entities.xml

