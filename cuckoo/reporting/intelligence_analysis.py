import os
import json
import codecs
import hashlib
import logging
import pickle
import numpy as np
from pprint import pprint

from cuckoo.common.abstracts import Report
from cuckoo.common.exceptions import CuckooReportError
from cuckoo.misc import cwd

from sklearn.ensemble import RandomForestRegressor


G_IA_INITIALIZED = None

G_IA_CALL_INDEX = None
G_IA_CALL_PAIR_INDEX = None


G_IA_RF_MODEL = None
G_IA_RF_FEATURE_LEN = None


class IntelligenceAnalysis(Report):
    """Saves analysis results in JSON format."""

    @staticmethod
    def init_static_resources():
        global \
            G_IA_INITIALIZED, \
            G_IA_CALL_PAIR_INDEX, \
            G_IA_CALL_INDEX, \
            G_IA_RF_FEATURE_LEN, \
            G_IA_RF_MODEL

        ia_file_dir = os.path.join(cwd(root=1), "intelligence_analysis")

        with open(os.path.join(ia_file_dir, "call_index.json"), "rb") as f:
            G_IA_CALL_INDEX = json.load(f)

        with open(os.path.join(ia_file_dir, "call_pair_index.json"), "rb") as f:
            G_IA_CALL_PAIR_INDEX = json.load(f)

        with open(os.path.join(ia_file_dir, "rfr_model.obj"), "rb") as f:
            G_IA_RF_MODEL = pickle.load(f)

        G_IA_RF_FEATURE_LEN = len(G_IA_CALL_INDEX) + len(G_IA_CALL_PAIR_INDEX)

        G_IA_INITIALIZED = True

    def run(self, results):
        """Writes report.
        @param results: Cuckoo results dict.
        @raise CuckooReportError: if fails to write report.
        """
        try:
            if not G_IA_INITIALIZED:
                self.init_static_resources()

            self.call_index_cache = G_IA_CALL_INDEX

            results.get("behavior", {}).get("processes", {})

            result_doc = {}

            call_doc_list_by_process = self.get_process_call_list(results)

            # call sequence generator (only syscall_num)
            result_doc["call_list"], \
            result_doc["call_list_len"], \
            result_doc["call_statics"] = self.call_sequence_generator(
                call_doc_list_by_process
            )
            result_doc["call_pair"] = self.call_pair_generator(
                call_doc_list_by_process
            )

            rfr_predicted, feature_vec = self.rfr_model(result_doc)

            results["intelligence"] = {}
            results["intelligence"]["rfr_predicted"] = rfr_predicted
            results["intelligence"]["rfr_feature_vec"] = feature_vec

            results["info"]["ia_score"] = float("%.1f" % (10 * rfr_predicted))

        except (UnicodeError, TypeError, IOError) as e:
            raise CuckooReportError("Failed to generate JSON report: %s" % e)

    def rfr_model(self, result_doc):
        x = np.zeros(G_IA_RF_FEATURE_LEN)

        # get call pair
        for call_pair, call_pair_num in result_doc["call_pair"].items():
            if call_pair not in G_IA_CALL_PAIR_INDEX:
                continue
            x[len(G_IA_CALL_INDEX) + G_IA_CALL_PAIR_INDEX[call_pair] - 1] += call_pair_num

            # get call statics
        for call_id, call_num in result_doc["call_statics"].items():
            x[int(call_id) - 1] = call_num
        # call pair generator
        predicted = G_IA_RF_MODEL.predict(x.reshape(1, -1))
        return predicted[0], list(x)

    def get_process_call_list(self, results):
        call_doc_list_by_process = []
        for process_doc in results.get("behavior", {}).get("processes", {}):
            call_doc_list = []
            for call_doc in process_doc["calls"]:
                call_id = self.call_name_to_id(call_doc["api"])
                if not call_id:
                    continue
                call_doc["index"] = call_id
                call_doc_list.append(call_doc)
            # No need to sort here
            # call_doc_list.sort(key=lambda x: x["time"])

            call_doc_list_by_process.append(call_doc_list)
        return call_doc_list_by_process

    @staticmethod
    def call_sequence_generator(call_doc_list_by_process):
        call_list = list()
        call_statics = dict()
        for call_doc_list in call_doc_list_by_process:
            for call_doc in call_doc_list:
                # call_id = self.call_name_to_id(call_doc["api"])
                call_list.append((
                    call_doc["index"], call_doc["time"]
                ))

                key = str(call_doc["index"])
                if key not in call_statics:
                    call_statics[key] = 1
                else:
                    call_statics[key] += 1

        call_list.sort(
            key=lambda x: x[1]
        )
        call_list = list(map(lambda x: x[0], call_list))
        return call_list, len(call_list), call_statics

    def call_name_to_id(self, call_name):
        if call_name not in self.call_index_cache:
            return None
        return self.call_index_cache[call_name]

    def call_pair_generator(self, call_doc_list_by_process):
        record = {}
        for call_doc_list in call_doc_list_by_process:
            hashed_args_list = list(
                map(
                    lambda x: (
                        x["index"],
                        self.get_hashed_args_set(x)
                    ),
                    call_doc_list
                )
            )
            # print(len(hashed_args_list))
            for i in range(1, len(hashed_args_list)):
                # print(i)
                # print("call id: ", hashed_args_list[i][0])
                for j in range(max(0, i - 100), i):
                    if hashed_args_list[i][1] & hashed_args_list[j][1]:
                        # print(call_doc_list[i])
                        # print(call_doc_list[j])
                        # print("%d - %d" % (i, j))
                        key = "%s-%s" % (
                            hashed_args_list[i][0],
                            hashed_args_list[j][0]
                        )
                        # print(key)
                        value = record.get(key, None)
                        if not value:
                            record[key] = 1
                        else:
                            record[key] = value + 1
        return record

    @staticmethod
    def get_hashed_args_set(call_doc):

        arg_set = set()
        for arg in call_doc["arguments"].values():
            md5_str = ""
            if type(arg) == unicode:
                try:
                    md5_str = hashlib.md5(arg.encode("unicode-escape")).hexdigest()
                except Exception:
                    logging.error("Md5 error")
            else:
                md5_str = hashlib.md5(str(arg)).hexdigest()
            arg_set.add(
                md5_str
            )
        return arg_set

    @staticmethod
    def syscall_association(arg_set_x, arg_set_y):
        if arg_set_x & arg_set_y:
            return True
        return False
