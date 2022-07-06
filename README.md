# Setup

See [the original readme for more information](./OG_README.md).

I'm running Python 3.8 for some clarity. And I've updated the dependencies of this repo.

To get set up, run the following:

```bash
sh setup.sh
```

Alternatively:

```bash
chmod +x setup.sh && ./setup.sh
```

Then run the following to install dependencies:

```bash
. venv/bin/activate
pip install -r code/requirements.txt
```

Once set up, you should be able to train the models.

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

To use a gpu, you can add the `-gpu` flag to the end of any `run.sh` script command:


```bash
sh run.sh 50 cv_asdiv-a -gpu 0
```

To see help for any command (in the case of wanting to modify a `run.sh` with other model params), add the `-h` flag to the end of any `run.sh` script command:

```bash
sh run.sh 50 cv_asdiv-a -h
```

#  Testing Adversarial Attacks

From what I can tell, adversary "attacks" could be implemented in each `data/*/test.csv`. These are the files used in testing.

You'll need to make sure each `data/*/train.csv` and `data/*/dev.csv` are exclusive (no duplication), then the easiest thing to do is make a copy of each `data/*/dev.csv`
and do whatever adversarial "attack" you're testing on those examples, naming it `data/*/test.csv`. See [data/cv_asdiv-a/fold0/test.csv](./data/cv_asdiv-a/fold0/test.csv) for a reference.

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
# Specify test and the dataset
sh run.sh test cv_asdiv-a
```

## Transformer Seq2Seq

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
# Specify test and the dataset
sh run.sh test cv_asdiv-a
```

## GTS

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
# Specify test and the dataset
sh run.sh test cv_asdiv-a
```

## Graph2Tree

First move to the Graph2Tree directory:

```bash
cd code/graph2tree
```

To train:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

Once you have a trained model in the `models/` directory test like this:

```bash
# Specify test and the dataset
sh run.sh test cv_asdiv-a
```

## Constrained

First move to the Constrained directory:

```bash
cd code/constrained
```

To train:

```bash
# Specify the number of epochs and the dataset
sh run.sh 50 cv_asdiv-a
```

Once you have a trained model in the `models/` directory test like this:

```bash
# Specify test and the dataset
sh run.sh test cv_asdiv-a
```
