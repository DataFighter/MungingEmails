__author__ = 'alex'

from fuzzywuzzy import fuzz
from email_datatypes import Email
from email_getter import FileCreator
from email_datatypes import Collection
import cPickle as pickle
from profile import Contact
from profile import Profile
from profile import ProfileStorage
import os
import time
import sys
from bs4 import BeautifulSoup
from profile import Name
import json

#
# def test_against_turked_set():
#     profiles.append(Profile(Contact("Alex K Godwin", "")))
#     for l in open("test.txt", "r").readlines():
#         con = Contact(l, "")
#         has_match = False
#         for idx, profile in enumerate(profiles):
#             if profile.contact_matches_profile(con):
#                 print "This contact:", con, "matched:", profile.get_contacts()
#                 profile.add_contact(con)
#                 print profile.get_contacts()
#                 has_match = True
#         if not has_match:
#             p = Profile(con)
#             print "Created profile: ", p
#             profiles.append(p)
#     print "------"
#     for profile2 in profiles:
#         print "List: ", profile2.get_contacts()
#         print "Av:", profile2.get_average_contact()
#
#     ids = []
#     turked_emails = json.load(open("data_files/turked_data.json"))
#     for x in turked_emails['items']:
#         ids.append(x['id'])
#     num_from = 0
#     for id_num in ids:
#         id_to_check = 0
#         e = Email(open("/Users/alex/Dropbox/Alex's Folder/HRCEmails/test/" + id_num + ".pdf.txt").readlines())
#         # idx_to_check = 0
#         for idx, email in enumerate(turked_emails['items']):
#             if email['id'] == id_num:
#                 idx_to_check = idx
#                 break
#         a = Contact(e.get_from().strip(), "(This info has been redacted)")
#         py_email = str(BeautifulSoup(a.get_email_address().get_whole()))
#         py_name = a.get_name()
#         turked_email = str(BeautifulSoup(turked_emails['items'][idx_to_check]['results']['sender-email-address']))
#         turked_name = str(BeautifulSoup(turked_emails['items'][idx_to_check]['results']['sender-name']))
#         print_correct = True
#         if fuzz.ratio(py_email.replace("(This info has been redacted)", "").strip(), turked_email) > 90:
#             num_from += 1
#             # print a.get_email_address(), ":", turked_emails['items'][idx_to_check]['results']['sender-email-address']
#         elif py_name.compare_to(Name(turked_name)) > 90:
#             num_from += 1
#             # print a.get_name(), ":", turked_emails['items'][idx_to_check]['results']['sender-name']
#         elif a.get_email_address().get_redacted() and turked_email == "NOT FOUND":
#             num_from += 1
#             # print idx_to_check
#         elif a.get_name().get_redacted() and turked_name == "NOT FOUND":
#             num_from += 1
#         else:
#             print_correct = False
#         if not print_correct:
#             print turked_emails['items'][idx_to_check]['id']
#             print py_name.get_full_name(0), ":", turked_name
#             print py_email, ":", turked_email
#             print '-------------------------------------'
#
#     print float(num_from) / len(ids) * 100
#     print len(ids)


# docs_to_check = []
# for d in c:
#     if d.doc_should_be_checked():
#         docs_to_check.append(d.get_doc_id())
# print docs_to_check
# print len(docs_to_check)
# print "---------------------"
# create_initial_profiles(c, "data_files/profiles_pickle")
# num_of_cons = 0
# for p in profiles:
#     num_of_cons += len(p.get_contacts())
# num_emails = len(emails)
# print num_of_cons, ": ", num_emails
# merged_profiles = merge(profiles)
#
# pickle.dump(merged_profiles, open("data_files/profiles_pickle", "w"))
#
# print "---------------------"
# num_matched = 0
# num_redacted = 0
# num_not_matched = 0
# total_emails = 0
# c.set_debug(False)
# for d in c:
#     for idx, e in enumerate(d):
#         con = Contact(e.get_from(), "(This info has been redacted)")
#         matched = False
#         total_emails += 1
#         if not con.get_name().get_redacted() or not con.get_email_address().get_redacted():
#             for p in merged_profiles:
#                 if p.contact_in_profile(con):
#                     matched = True
#         else:
#             num_redacted += 1
#         if matched:
#             num_matched += 1
#
# print "total: ", total_emails
# print "redacted", num_redacted
# print "matched: ", num_matched
#
# empty_ids_clean = []
# [empty_ids_clean.append(x) for x in empty_ids if x not in empty_ids_clean]
# print empty_ids_clean
# print len(empty_ids)
# print len(empty_ids_clean)
# f = open("data_files/tester.json", "w")
# json.dump([p.get_dict() for p in merged_profiles], f, indent=4)
# f.close()
if __name__ == "__main__":
    col = Collection("hilary_text_files/", ".txt", True)
    col.set_debug(True)
    num_of_bad = []
    for d in col:
        if d.doc_should_be_checked():
            num_of_bad.append(d)
    print "\nNumber to be turked:", len(num_of_bad)
    start = time.time()
    ps = ProfileStorage(col, pickle_file="data_files/profile_pickle.pickle")
    print "Profile disambiguation time: ", (time.time() - start)
    to_app = []
    index = 0
    failed_contacts = []
    links = open("data_files/attachment.txt", "r").readlines()
    print "\nDumping data..."
    print "===================================="

    for idx1, d in enumerate(col):
        for line in links:
            if d.get_doc_id() in line:
                d.set_pdf_link(line)
        for idx2, e in enumerate(d):
            froms = []
            tos = []
            ccs = []
            try:
                for f in e.get_from().split(";"):
                    c = Contact(f, "(This info has been redacted)")
                    c.set_sanitize(True)
                    if not c.is_empty() and not c.is_redacted():
                        froms.append(str(ps.get_profile(c).get_average_contact()))
                for t in e.get_to().split(";"):
                    c = Contact(t, "(This info has been redacted)")
                    c.set_sanitize(True)
                    if not c.is_empty():
                        tos.append(str(ps.get_profile(c).get_average_contact()))
                for cc in e.get_cc().split(";"):
                    c = Contact(cc, "(This info has been redacted)")
                    c.set_sanitize(True)
                    if not c.is_empty():
                        ccs.append(str(ps.get_profile(c).get_average_contact()))
            except:
                failed_contacts.append(c)
            to_app.append({
                "id": index,
                "from_raw": e.get_from(),
                "to_raw": e.get_to(),
                "cc_raw": e.get_cc(),
                "from_displays": froms,
                "to_displays": tos,
                "cc": ccs,
                "subject": e.get_subject(),
                "body": e.get_body(),
                "date": e.get_sent(),
                "thread_id": idx1,
                "email_id": idx2,
                "state_dep_doc_id": d.get_doc_id(),
                "pdf_link": d.get_pdf_link()
            })
            index += 1
    f = open("data_files/to_eric.json", "w")
    json.dump(to_app, f)
    f.close()
    print "\nDone!"
    print "===================================="
