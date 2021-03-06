class Probability(object):
    def __init__(self, key, complemented, value):
        self.key = key
        self.complemented = complemented
        self.value = value

    def equals(self, probability):
        return self.key == probability.key and self.complemented == probability.complemented

    def to_string(self):
        complementedString = ""
        if self.complemented:
            complementedString = "-"
        return str(self.key) + complementedString


def compare(si,sj):
    # ako su disjunktni
    for probability1 in sj:
        cprobability1 = Probability(probability1.key, not probability1.complemented, probability1.value)
        for probability2 in si:
            if cprobability1.equals(probability2):
                return []
    # nadi elemente koji su u sj a nisu u si
    result = []
    for probability1 in sj:
        match = False
        for probability2 in si:
            if probability1.equals(probability2):
                match = True
                break
        if not match:
            result.append(probability1)
    return result


def printArrayOfProbs(x):
    result = ""
    for prob in x:
        result += "(" + prob.to_string() + ") "
    return result


def transform(probabilitiesAppending, otherProbabilities):
    if not probabilitiesAppending:
        return [otherProbabilities]
    result = []
    appending = []
    for probability in probabilitiesAppending:
        # complement last one in appending array
        if appending:
            appending[len(appending)-1] = Probability(appending[len(appending)-1].key,
                                                      not appending[len(appending)-1].complemented,
                                                      appending[len(appending) - 1].value)
        appending.append(Probability(probability.key, not probability.complemented, probability.value))
        result.append(list(appending) + list(otherProbabilities))

    return result


# this takes list of groped events for each path
def calculateAbrahamValueFromEvents(listOfPathEvents):
    nds = listOfPathEvents
    ds = []

    # move first element to ds
    ds.append(nds.pop(0))

    for si in nds:
        listOfEventsToCompare = [si]
        for sj in ds:
            listOfEventsToCompareTemporary = []
            for events in listOfEventsToCompare:
                transformed = transform(compare(events, sj), events)
                listOfEventsToCompareTemporary += transformed
            listOfEventsToCompare = list(listOfEventsToCompareTemporary)
        ds += listOfEventsToCompare

    # calculate final value
    finalValue = 0
    for events in ds:
        multiplication = 1
        for event in events:
            multiplication *= (1 - event.value) if event.complemented else event.value
        finalValue += multiplication
    return finalValue


# graph = object from networkx
# listOfPaths = list of lists containing integer (integer representing node number), sorted from shortest to longest!!
# valueComputing = attribute of node which contains value to compute (e.g. reliability)
# example of usage: abraham(G, [[1, 2, 4], [1, 3, 4], [1, 2, 3, 4], [1, 3, 2, 4]], 'R')
def abraham(graph, listOfPaths, valueComputing):
    listOfPathEvents = []
    for path in listOfPaths:
        pathEvents = []
        # turn edges into probabilities
        for i in range(len(path) - 1):
            if (i < len(path) - 1):
                edgeKey = str(path[i]) + str(path[i + 1]) + "e" if path[i] < path[i + 1] else str(path[i + 1]) + str(path[i]) + "e"
                pathEvents.append(Probability(edgeKey, False, graph.get_edge_data(path[i], path[i + 1])[valueComputing]))
        # turn nodes into probabilities
        for nodeNumber in path:
            pathEvents.append(Probability(nodeNumber, False, graph.node[nodeNumber][valueComputing]))
        listOfPathEvents.append(pathEvents)
    return calculateAbrahamValueFromEvents(listOfPathEvents)

