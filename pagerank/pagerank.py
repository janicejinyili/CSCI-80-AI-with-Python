import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    all_pages = set(corpus.keys())

    # probability contributed by damping
    damping_prob = (1 - damping_factor) / len(all_pages) 
    
    # if page doesn't link to any page
    if len(corpus[page]) == 0:
        prob = {p : damping_prob for p in all_pages}
    else:
        prob = dict()
        for p in all_pages:
            if p in corpus[page]:
                prob[p] = damping_prob + damping_factor / len(corpus[page])
            else:
                prob[p] = damping_prob
    
    #  normalise
    factor=1.0/sum(prob.values())
    normalised_prob = {i: j * factor for i, j in prob.items()}
    return normalised_prob

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #  Initialize set of all pages, current page and sample list
    all_pages = list(corpus.keys())
    current_page = random.choice(all_pages)
    all_samples = [current_page]
    
    #  generate N samples with the transition model and count frequencies of the pages
    for i in range(n - 1):
        distribution = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(list(distribution.keys()), weights = list(distribution.values()))[0]
        all_samples.append(next_page)
        current_page = next_page
    pagerank = {p: all_samples.count(p) for p in set(all_samples)}
    
    #  normalise
    factor = 1.0 / sum(pagerank.values())
    normalised_pagerank = {i: j * factor for i, j in pagerank.items()}
    return normalised_pagerank


    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #  Initialize set of all pages, reversed corpus and starting PR
    all_pages = set(corpus.keys())
    N = len(all_pages)
    reversed_corpus = linked_by(corpus)
    current_pagerank = {x: 1 / N for x in all_pages}
    
    # Iterate the algorithm
    while True:
        new_pagerank = {x: 0 for x in all_pages}
        for p in new_pagerank.keys():
            
            #  calculate PR of all pages that link to p to update the PR of p
            pagerank_i = 0
            for i in reversed_corpus[p]:
                if len(corpus[i]) == 0:
                    pagerank_i += current_pagerank[i] / len(all_pages)
                else:
                    pagerank_i += current_pagerank[i] / len(corpus[i])
            new_pagerank[p] = (1 - damping_factor) / N + pagerank_i * damping_factor
        
        #  normalise
        factor = 1.0 / sum(new_pagerank.values())
        new_pagerank = {i: j * factor for i, j in new_pagerank.items()}
        
        #  Set stop condition as less than 0.001 change of PR 
        finished = True
        for p, pr in new_pagerank.items():
            if abs(pr - current_pagerank[p]) > 0.001:
                finished = False
        if finished == True:
            return new_pagerank 
        current_pagerank = new_pagerank


    raise NotImplementedError



def linked_by(corpus):
    
    #  generate a dictionary in which each page corresponds to all pages it links to
    all_pages = set(corpus.keys())
    reversed_corpus = {x: set() for x in all_pages}
    for p1 in all_pages:
        for p2 in all_pages:
            if p1 in corpus[p2] or len(corpus[p2]) == 0:
                reversed_corpus[p1].add(p2)
    return reversed_corpus



if __name__ == "__main__":
    main()
