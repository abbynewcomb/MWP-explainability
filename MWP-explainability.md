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

Each model is basically copy pasta of the last.

This is an example the author gives to run the RNN model:

```bash
python -m src.main -mode train -embedding roberta -emb_name roberta-base -emb1_size 768 -hidden_size 256 -depth 2 -lr 0.0002 -emb_lr 8e-6 -batch_size 4 -epochs 50 -dataset cv_asdiv-a -full_cv -run_name run_cv_asdiv-a
```

Since this command is pretty long, the equivalent using a relative `run.sh` script is:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

To use a gpu, you can add the `-gpu` flag to the end:


```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a -gpu 0
```

Once set up, you should be able to train the models.

From what I can tell, adversary "attacks" could be implemented in each `data/*/test.csv`. These are the files used in testing.

You'll need to make sure each `data/*/train.csv` and `data/*/dev.csv` are exclusive (no duplication), then the easiest thing to do is make a copy of each `data/*/dev.csv`
and do whatever adversarial "attack" you want to test on those examples, naming it `data/*/test.csv`.

## RNN Seq2Seq

First move to the RNN Seq2Seq directory:

```bash
cd code/rnn_seq2seq
```

To train:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

Once you have a trained model in the `models/` directory test like this:

```bash
# Specify the number of epochs and the dataset
sh run.sh test cv_asdiv-a
```

# Transformer Seq2Seq

I set this up to be the same as the "Attention Is All You Need" paper. You'll probably want to adjust the params in `run.sh`.

First move to the Transformer Seq2Seq directory:

```bash
cd code/transformer_seq2seq
```

To train:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

Once you have a trained model in the `models/` directory test like this:

```bash
# Specify the number of epochs and the dataset
sh run.sh test cv_asdiv-a
```

# GTS

First move to the GTS directory:

```bash
cd code/gts
```

To train:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

Once you have a trained model in the `models/` directory test like this:

```bash
# Specify the number of epochs and the dataset
sh run.sh test cv_asdiv-a
```

