import shelve


class GameStatistics:
    def __init__(self, filename):
        self._filename = filename

    def save_record(self, score, name):
        with shelve.open(self._filename) as records:
            if name not in records.keys():
                records[name] = score
            elif records[name] <= score:
                records[name] = score

    def get_records(self):
        with shelve.open(self._filename) as f:
            records = sorted(f.items(), key=lambda x: x[1], reverse=True)[:15]
            return records


def reset_statistics(filename):
    with shelve.open(filename) as f:
        f.clear()


if __name__ == '__main__':
    print("send Y if you want to reset records")
    temp = input()
    if temp == "Y":
        reset_statistics("records")
        print("records were reset")
