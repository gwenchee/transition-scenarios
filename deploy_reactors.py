import csv
import jinja2
import os
import sys

if len(sys.argv) < 4:
    print('Usage: python deploy_reactors.py [fleet]\
          [BuildtimeTemplate] [Reactor1] [Reactor2] ...')


def import_csv(in_csv):
    with open(in_csv, 'r') as source:
        sourcereader = csv.reader(source, delimiter='\t')
        data_list = []
        for row in sourcereader:
            data_list.append(row)
    return data_list


def load_template(in_template):
    with open(in_template, 'r') as default:
        output_template = jinja2.Template(default.read())
    return output_template


def get_build_time(in_list, *args):
    data_dict = {}
    for col, item in enumerate(in_list):
        start_date = [in_list[col][11], in_list[col][9], in_list[col][10]]
        month_diff = int((int(start_date[0])-1965) * 12 +
                         int(start_date[1]) +
                         int(start_date[2]) / (365/12))
        for index, reactor in enumerate(args[0][0]):
            fleet_name = in_list[col][0].replace(' ', '_')
            file_name = reactor.replace(os.path.dirname(args[0][0][index]), '')
            file_name = file_name.replace('/', '')
            if (fleet_name + '.xml' == file_name):
                data_dict.update({fleet_name: month_diff})
    return data_dict


def make_recipe(in_dict, in_template):
    reactor_list = in_dict.keys()
    buildtime_list = in_dict.values()
    rendered = in_template.render(reactors=reactor_list,
                                  buildtimes=buildtime_list)
    with open('cyclus_input/buildtimes/buildtimes.xml', 'w') as output:
            output.write(rendered)


def main(in_csv, in_template, *args):
    if os.path.isdir(args[0][0]):
        lists = []
        for files in os.listdir(args[0][0]):
            lists.append(args[0][0] + files)
        main(in_csv, in_template, lists)
    else:
        fleet_list = import_csv(in_csv)
        buildtime_template = load_template(in_template)
        buildtime_dict = get_build_time(fleet_list, args)
        make_recipe(buildtime_dict, buildtime_template)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
