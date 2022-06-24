# Setup

I'm running Python 3.8 for some clarity. And I've updated the dependencies of this repo.

To get set up, run the following:

```bash
sh setup.sh
```

Alternatively:

```bash
chmod +x setup.sh && ./setup.sh
```

# Running The Code

I'd try to closely follow how the SVAMP paper lays out their training. You'll most-likely need to hit a similar benchmark in training as described in their paper (for each model).

## RNN Seq2Seq

Once set up, you should be able to run the following to train a model:

```bash
cd code/rnn_seq2seq
```

```bash
python -m src.main -mode train -embedding roberta -emb_name roberta-base -emb1_size 768 -hidden_size 256 -depth 2 -lr 0.0002 -emb_lr 8e-6 -batch_size 4 -epochs 50 -dataset cv_asdiv-a -full_cv -run_name run_cv_asdiv-a
```

Since this command is pretty long, the equivalent using the `run.sh` script is:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

Similarly to test the trained model:

```bash
# Specify the number of epochs and the dataset
sh run.sh test cv_asdiv-a
```
