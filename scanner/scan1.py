# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys, getopt, ntpath

reload(sys)
sys.setdefaultencoding('utf8')
browser_drivers = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
    "IE": webdriver.Ie
}
# webPage = "http://seleniumhq.org/"
# webPage = "http://vhi.ie/"
# webPage = "http://newtours.demoaut.com"
# webPage = "http://bbc.co.uk/"

def main(argv):
    inputfile = ''
    outputfile = ''

    filename = ""
    browser_to_use = ""

    try:
        filename = ntpath.basename(argv[0])  # lop off the path from the file name
        opts, args = getopt.getopt(argv[1:], "h:i:o:b:", ["ifile=", "ofile=", "browser="])
    except getopt.GetoptError:
        print("Usage: {} -i <inputfile> -o <outputfile> -b <browser>".format(filename))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: {} -i <inputfile> -o <outputfile> -b <browser>".format(filename))
            sys.exit()
        elif opt in ("-b", "--browser"):
            browser_to_use = arg
            print("Browser is {}".format(browser_to_use))
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            print("Input file is {}".format(inputfile))
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            print("Output file is {}".format(outputfile))
    fileout = open(outputfile, 'w')

    browser_driver = browser_drivers[browser_to_use]()
    browser_driver.get("{}".format(inputfile))
    sleep(10)
    browser_driver.maximize_window()
    # browser_driver.get(webPage)

    # The element type and  list of the attributes to use to generate the xpath expression
    # The attributes can be replaced or added to suit applications
    element_attribute_list = [
        ["link", "id", "rel", "href", "class"],
        ["a", "id", "text", "class"],
        ["button", "id", "type", "class", "text"],
        ["input", "id", "name", "type", "placeholder"],
        ["img", "id", "alt", "class", "src"]
    ]
    for elem_type in element_attribute_list:
        attribute = "//" + elem_type[0]

        # get a list of all elements of this type
        all_elements = browser_driver.find_elements_by_xpath(attribute)
        # print "Found total of {} <{}>  elements".format(len(allElements), a[0])

        el_count = 0
        for element in all_elements:
            el_count += 1
            xpath = xpath_generate(elem_type, element)

            # Evaluate the xpath expression if it's not empty
            if xpath != "":
                try:
                    instance_count = len(browser_driver.find_elements_by_xpath(xpath))
                except NoSuchElementException:
                    print ("!!! Bad expression -> {}", xpath)
                print("Xpath expression {} found {} elements".format(xpath, instance_count))
                if instance_count == 1:             # If one instance found, we already have a unique expression
                    continue

                # Look for nearest ancestor with an ID attribute
                attrib = "@id"
                ancestors = browser_driver.find_elements_by_xpath(xpath + "/ancestor::*[{}][1]".format(attrib))
                if len(ancestors) == 0:
                    # Look for nearest ancestor with a name attribute
                    attrib = "@name"
                    ancestors = browser_driver.find_elements_by_xpath(xpath + "/ancestor::*[{}][1]".format(attrib))
                    if len(ancestors) == 0:
                        # Look for nearest ancestor with a text attribute
                        attrib = "text()"
                        ancestors = browser_driver.find_elements_by_xpath(xpath + "/ancestor::*[{}][1]".format(attrib))

                for ancestor in ancestors:
                    variable_name = "{}_{}_{}".format(ancestor.tag_name, ancestor.get_attribute("id"), elem_type[0])
                    print(
                        "...Unique locator is {}".format(variable_name) + "=\"//{}[{}='{}']{}\""
                        .format(ancestor.tag_name, attrib, ancestor.get_attribute("id"), xpath))
                    # If not unique yes, then need to go bak up more

    browser_driver.close()
    fileout.close()


# Generate an xpath expression based on the attributes of a element and their values
def xpath_generate(a, e):
    # print ("#{}  <{}> ".format(el_count, a[0]).encode('utf-8', 'ignore'))
    elementtype = a[0]
    x_path_id = ""
    a = a[1:]  # remove element type so only attribute remain
    attrib_count = 0
    for attrib in a:
        # attrib_value = e.get_attribute(attrib)
        attrib_value = e.get_property(attrib)
        if attrib_value == "":
            # attrib_value = "NULL"
            continue  # ignore empty attributes
        attrib_count += 1
        if attrib == "text":
            attrib = "text()"
        else:
            attrib = "@" + attrib
        # print (" <{}>=={}".format(attrib, attrib_value)).encode('utf-8', 'ignore')
        if attrib_count > 1:
            # print "count={} length={}".format(attrib_count, len(a))
            x_path_id += " and "
        x_path_id = x_path_id + '{}="{}"'.format(attrib, attrib_value).encode('utf-8', 'ignore')

    if x_path_id != "":
        x_path_id = "//{}[{}]".format(elementtype, x_path_id)

    # print "XPath ID is: " + xPathId
    return x_path_id


if __name__ == "__main__":
    main(sys.argv[0:])
