
import sys
import unittest

from multiprocessing import Queue

from mojo.xmods.xmultiprocessing.pipedprocess import PipedProcess

def test_producer(action_queue, response_queue):

    while True:
        action = action_queue.get()
        if action == "echo":
            print("Action Echo")
            response_queue.put("Echo")
        else:
            print(f"Error {action}.", file=sys.stderr)
            response_queue.put("Error")


class TestStrToByteConversions(unittest.TestCase):

    def test_str_to_bytes_conversion(self):

        action_queue = Queue()
        response_queue = Queue()

        rmtproc = PipedProcess(target=test_producer, args=(action_queue, response_queue), daemon=True)
        rmtproc.start()
        
        try:
            action_queue.put("echo")
            resp = response_queue.get(timeout=10)
            print(f"resp: {resp}")

            action_queue.put("blah")
            resp = response_queue.get(timeout=10)
            print(f"resp: {resp}")
        
        finally:
            rmtproc.terminate()
            rmtproc.join()
            rmtproc.close()

        return

if __name__ == '__main__':
    unittest.main()
