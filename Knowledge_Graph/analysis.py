data_file = "movies.nt"
language_tag = "@en-US"
line_ending = " ."

predicate_has_type = "<http://adelaide.edu.au/dbed/hasType>"
predicate_has_name = "<http://adelaide.edu.au/dbed/hasName>"
predicate_has_actor = "<http://adelaide.edu.au/dbed/hasActor>"
uri_person = "<http://adelaide.edu.au/dbed/Person>"
predicate_prefix = "<http://adelaide.edu.au/dbed/has"


def _is_uri(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("<") and some_text.endswith(">")

def _is_blank_node(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("_:")

def _is_literal(some_text):
    return some_text.startswith("\"") and some_text.endswith("\"")
    
def _parse_line(line):
    # this could be done using regex
    
    # for each line, remove newline character(s)
    line = line.strip()
    #print(line)
    
    # throw an error if line doesn't end as required by file format
    assert line.endswith(line_ending), line
    # remove the ending part
    line = line[:-len(line_ending)]
    
    # find subject
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into subject and the rest
    s = line[:i]
    
    line = line[(i + 1):]
    # throw an error if subject is neither a URI nor a blank node
    assert _is_uri(s) or _is_blank_node(s), s

    # find predicate
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into predicate and the rest
    p = line[:i]
    line = line[(i +1):]
    # throw an error if predicate is not a URI
    assert _is_uri(p), str(p)
    
    # object is everything else
    o = line
    
    # remove language tag if needed
    if o.endswith(language_tag):
        o = o[:-len(language_tag)]

    # object must be a URI, blank node, or string literal
    # throw an error if it's not
    assert _is_uri(o) or _is_blank_node(o) or _is_literal(o), o
    
    #print([s, p, o])
    
    return s, p, o

def _compute_stats1():
    # ... you can add variables here ...
    n_triples = 0 # triple
    n_people = set()
    actor_appearances = {}
    actor_names = {}
    actor_movies = {}

    # open file and read it line by line
    # assume utf8 encoding, ignore non-parseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            # print('line:', line)
            # break
            s, p, o = _parse_line(line)
            
            # print('s:', s)
            # print('p:', p)
            # print('o:', o) 
            # break
                
    ###########################################################
    # ... your code here ...
    # you can add functions and variables as needed;
    # however, do NOT remove or modify existing code;
    # _compute_stats() must return four values as described;
    # you can add print statements if you like, but only the
    # last four printed lines will be assessed;
    ###########################################################
            # Count distinct triples
            n_triples += 1
            # Check if the object is a person (URI) and add them to the set of people
            if _is_uri(o) and o == uri_person:
                n_people.add(s) 
            
            # Check if the predicate is "hasActor" and collect actor appearances
            if p == predicate_has_actor:
                if o not in actor_appearances:
                    actor_appearances[o] = 1
                else:
                    actor_appearances[o] += 1
                    
                if o in actor_movies:
                    actor_movies[o].add(s)
                else: 
                    actor_movies[o] = {s}
    
        #if s.startswith("_:p_") and p == predicate_has_name:
        if _is_blank_node(s) and p == predicate_has_name:
                actor_names[s] = o
                
    # actor_appearances
    # :p --> key 
    # value count of movies 
    # predicion has actor 
    
                 
    ###########################################################
    # n_triples -- number of distinct triples
    # n_people -- number of distinct people mentioned in ANY role
    #             (e.g., actor, director, producer, etc.)
    # n_top_actors -- number of people appeared as ACTORS in
    #                 M movies, where M is the maximum number
    #                 of movies any person appeared in as an actor
    # n_highweight_actor -- the 'weight' of an actor is calculated by 
    #               dividing each 'appearance' by their place in 
    #               the cast list. If we add up all of these, we
    #               get the cumulative weight of the actor. The 
    #               'highweight' is the largest cumulative weight.
    # s_name -- the name of the highweight actor
    ###########################################################
    
     # Calculate the number of top actors (actors with the most appearances)
    #n_top_actors = max(actor_appearances.values()) if actor_appearances else 0
    
       # Calculate the number of top actors (actors with the most appearances in different movies)
    if actor_movies:
        max_appearances = max(len(movies) for movies in actor_movies.values())
        n_top_actors = sum(1 for movies in actor_movies.values() if len(movies) == max_appearances)
    else:
        n_top_actors = 0
    
     # Calculate the actor with the highest cumulative weight
    n_highweight_actor = None
    max_cumulative_weight = 0

    for actor, appearances in actor_appearances.items():
        if appearances <= 1:
            continue  # Skip actors with <= 1 appearance
        cumulative_weight = appearances / (appearances - 1)
        if cumulative_weight > max_cumulative_weight:
            max_cumulative_weight = cumulative_weight
            n_highweight_actor = actor

    # Retrieve the name of the highweight actor if available
    # s_name = actor_names.get(n_highweight_actor, "N/A")
    s_name = None
    for actor_id, actor_name in actor_names.items():
        if actor_id == n_highweight_actor:
            s_name = actor_name
    
    n_people  = len(n_people)
    
    # n_highweight_actor = len(n_highweight_actor)
    
    return n_triples, n_people, n_top_actors, n_highweight_actor, s_name


def _compute_stats():
    # ... you can add variables here ...

    n_triples = 0
    # n_people = set()
    people = {}

    n_top_actors_dict = {}
    top_val = 0
    n_top_actors = 0
    movies = {}
    actors = {}
    n_highweight_actor = 0

    # open file and read it line by line
    # assume utf8 encoding, ignore non-p    arseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            s, p, o = _parse_line(line)

            n_triples += 1
            
            # if _is_uri(o) and o == uri_person:
            #     n_people.add(s) 
                
                
            if (s.find("_:p") >= 0 and _is_literal(o)):
                # print(o)
                people[s] = o


            if (s.find("_:m") >= 0 and p.find("hasTitle") >= 0):
                movies[o] = []

            if (p.find("hasActor") >= 0):
                if (o in n_top_actors_dict):
                    n_top_actors_dict[o] += 1
                    if (top_val == n_top_actors_dict[o]):
                        n_top_actors += 1
                    elif (top_val < n_top_actors_dict[o]):
                        top_val = n_top_actors_dict[o]
                        n_top_actors = 1
                else:
                    n_top_actors_dict[o] = 1

                highweight = 0
                if (s in movies):
                    highweight = 1/len(movies[s])
                    movies[s].append(o)
                else:
                    highweight = 1
                    movies[s] = [o]

                if (o in actors):
                    actors[o][1] += highweight
                else:
                    actors[o] = [o, highweight]

                if (actors[o][1] > n_highweight_actor):
                    n_highweight_actor = actors[o][1]
                    s_name = o


    # n_people = len(n_people)
    n_people = len(people)
    s_name = people[s_name]

    return n_triples, n_people, n_top_actors, n_highweight_actor, s_name


# DO NOT CHANGE THE FINAL OUTPUT FORMATTING BELOW THIS LINE
if __name__ == "__main__":
    n_triples, n_people, n_top_actors, n_highweight_actor, s_name = _compute_stats()
    print()
    print(f"{n_triples:,} (n_triples)")
    print(f"{n_people:,} (n_people)")
    print(f"{n_top_actors} (n_top_actors)")
    print(f"{n_highweight_actor} (n_highweight_actor)")
    print(f"{s_name} (s_name)")
