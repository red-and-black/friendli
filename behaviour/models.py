from django.db import models


class BehaviourReport(models.Model):
    NOT_REVIEWED = 'not_reviewed'
    UNDER_REVIEW = 'under_review'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (NOT_REVIEWED, 'Not reviewed'),
        (UNDER_REVIEW, 'Under review'),
        (COMPLETED, 'Completed')
    )

    # Automatic timestamping fields.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Report
    reporter = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='reporter'
    )
    reportee = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='reportee'
    )
    report = models.TextField(max_length=2000)

    # Outcome/handling
    public_outcome = models.CharField(max_length=255, blank=True)
    private_outcome = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=NOT_REVIEWED
    )

    class Meta:
        ordering = ['-modified']
