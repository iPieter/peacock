I was doing some masked language modeling training with some old code and I got a strange error that took a long time to debug:

```
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

Eventually I located the root of this bug: the AdamW optimizer from HuggingFace, which is deprecated, caused it. For completeness, this was the call and the specific learning rate schedule that I had using Pytorch-Lightning.

```python
from torch.optim.lr_scheduler import LambdaLR
from transformers import (
    AdamW,
    get_linear_schedule_with_warmup,
)

def configure_optimizers(self):
    "Prepare optimizer and schedule (linear warmup and decay)"
    model = self.student
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": self.hparams.weight_decay,
        },
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]
    optimizer = AdamW(
        optimizer_grouped_parameters,
        lr=self.hparams.learning_rate,
        eps=self.hparams.adam_epsilon,
    )

    scheduler = {
        "scheduler": LambdaLR(
            optimizer,
            lr_lambda=LRPolicy(
                self.hparams.warmup_steps,
                self.trainer.estimated_stepping_batches,
            ),
        ),
        "interval": "step",
        "frequency": 1,
        "name": "learning_rate",
    }
    return [optimizer], [scheduler]
```

The only thing that needs to change is the import of AdamW:

```diff
from transformers import (
-    AdamW,
    get_linear_schedule_with_warmup,
)
+from torch.optim import AdamW
```

Since the error of this bug led me down completely the wrong path, I decided that a (hopefully) findable blog post could be helpful.