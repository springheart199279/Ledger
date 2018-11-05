# Generated by Django 2.1.1 on 2018-11-02 01:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_ledger.models.io.generic
import django_ledger.models.io.preproc
import jsonfield.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.CharField(max_length=5, unique=True, verbose_name='Account Code')),
                ('name', models.CharField(max_length=100, verbose_name='Account Name')),
                ('role', models.CharField(choices=[('Assets', (('ca', 'Current Asset'), ('lti', 'Long Term Investments'), ('ppe', 'Property Plant & Equipment'), ('ia', 'Intangible Assets'), ('aadj', 'Asset Adjustments'))), ('Liabilities', (('cl', 'Current Liabilities'), ('ltl', 'Long Term Liabilities'))), ('Equity', (('cap', 'Capital'), ('cadj', 'Capital Adjustments'), ('in', 'Income'), ('ex', 'Expense'))), ('Other', (('excl', 'Excluded'),))], max_length=10, verbose_name='Account Role')),
                ('role_bs', models.CharField(max_length=20, null=True, verbose_name='Balance Sheet Role')),
                ('balance_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=6, verbose_name='Account Balance Type')),
                ('locked', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.AccountModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChartOfAccountModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('desc', models.TextField(verbose_name='CoA Description')),
            ],
            options={
                'verbose_name': 'Chart of Account',
            },
        ),
        migrations.CreateModel(
            name='CoAAccountAssignments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locked', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coa_assignments', to='django_ledger.AccountModel', verbose_name='Accounts')),
                ('coa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_assignments', to='django_ledger.ChartOfAccountModel', verbose_name='Chart of Accounts')),
            ],
            options={
                'verbose_name': 'Chart of Account Assignment',
            },
        ),
        migrations.CreateModel(
            name='EntityModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('coa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_ledger.ChartOfAccountModel', verbose_name='Chart of Accounts')),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
        ),
        migrations.CreateModel(
            name='JournalEntryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('desc', models.CharField(blank=True, max_length=70, null=True)),
                ('freq', models.CharField(choices=[('nr', 'Non-Recurring'), ('d', 'Daily'), ('m', 'Monthly'), ('q', 'Quarterly'), ('y', 'Yearly'), ('sm', 'Monthly Series'), ('sy', 'Yearly Series')], max_length=2)),
                ('activity', models.CharField(choices=[('op', 'Operating'), ('fin', 'Financing'), ('inv', 'Investing'), ('other', 'Other')], max_length=5)),
                ('origin', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LedgerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('scope', models.CharField(choices=[('a', 'Actual'), ('f', 'Forecast'), ('b', 'Baseline')], max_length=1)),
                ('years_horizon', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledgers', to='django_ledger.EntityModel')),
            ],
            options={
                'verbose_name': 'Ledger',
                'abstract': False,
            },
            bases=(models.Model, django_ledger.models.io.preproc.IOPreProcMixIn, django_ledger.models.io.generic.IOGenericMixIn),
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('params', jsonfield.fields.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='txs', to='django_ledger.AccountModel')),
                ('journal_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='txs', to='django_ledger.JournalEntryModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='journalentrymodel',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jes', to='django_ledger.LedgerModel'),
        ),
        migrations.AddField(
            model_name='journalentrymodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.JournalEntryModel'),
        ),
        migrations.AddField(
            model_name='chartofaccountmodel',
            name='accounts',
            field=models.ManyToManyField(related_name='coas', through='django_ledger.CoAAccountAssignments', to='django_ledger.AccountModel'),
        ),
        migrations.AddIndex(
            model_name='coaaccountassignments',
            index=models.Index(fields=['account', 'coa'], name='django_ledg_account_40ac57_idx'),
        ),
    ]
