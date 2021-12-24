from draft_parse import get_draft_data
from draft_rank import generate_position_ranks

if __name__ == "__main__":
    draft_picks = get_draft_data("data/2021")
    ranks = generate_position_ranks(draft_picks)
    print(ranks)