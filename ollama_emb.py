import ollama

model = "mxbai-embed-large"

embed = ollama.embed(
    model=model,
    input="Jim Butcher, the #1 New York Times bestselling author of The Dresden Files and the Codex Alera novels, conjures up a new series set in a fantastic world of noble families, steam-powered technology, and magic-wielding warriorsâ¦ Since time immemorial, the Spires have sheltered humanity, towering for miles over the mist-shrouded surface of the world. Within their halls, aristo Jim Butcher, the #1 New York Times bestselling author of The Dresden Files and the Codex Alera novels, conjures up a new series set in a fantastic world of noble families, steam-powered technology, and magic-wielding warriorsâ¦ Since time immemorial, the Spires have sheltered humanity, towering for miles over the mist-shrouded surface of the world. Within their halls, aristocratic houses have ruled for generations, developing scientific marvels, fostering trade alliances, and building fleets of airships to keep the peace. Captain Grimm commands the merchant ship,  . Fiercely loyal to Spire Albion, he has taken their side in the cold war with Spire Aurora, disrupting the enemyâs shipping lines by attacking their cargo vessels. But when the   is severely damaged in combat, leaving captain and crew grounded, Grimm is offered a proposition from the Spirearch of Albionâto join a team of agents on a vital mission in exchange for fully restoring   to its fighting glory. And even as Grimm undertakes this dangerous task, he will learn that the conflict between the Spires is merely a premonition of things to come. Humanityâs ancient enemy, silent for more than ten thousand years, has begun to stir once more. And death will follow in its wakeâ¦",
)

print(embed)
