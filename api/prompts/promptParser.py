def promptGenerator(promptName, variableDict):
    with open('prompts/'+promptName, 'r') as f:
        rawPrompt = f.read()

    variableNames = set(var.split('}}')[0] for var in rawPrompt.split('{{') if '}}' in var)

    text = rawPrompt
    for variableName in variableNames:
        if variableName in variableDict:
            text = text.replace('{{' + variableName + '}}', variableDict[variableName])
    return text
