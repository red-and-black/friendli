from collections import (
    Counter,
    OrderedDict,
)
from datetime import (
    datetime,
    timedelta,
)

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import F

from behaviour.models import BehaviourReport
from conferences.models import Conference
from conversations.models import Conversation
from meetups.models import Meetup
from profiles.models import (
    Blocked,
    Language,
    LookingFor,
    PersonalInterest,
    ProfessionalInterest,
    Profile,
    Starred,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Generates a report about the instance's usage.

        It assumes that the superuser is user 1, and that there are two people
        running the instance as administrators who are users 2 and 3. Users 1,
        2 and 3 together are referred to as admins in this management command,
        and are excluded from the statistics unless explicitly included.
        """
        # Initial
        date_format = '%d %b %Y'
        conference = Conference.objects.get()

        # Headers
        header_text = ('Friendli usage for %s' % conference.name)
        header_border = "*" * len(header_text)
        print()
        print(header_border)
        print(header_text)
        print(
            '%s - %s' % (
                conference.start_date.strftime(date_format),
                conference.end_date.strftime(date_format)
            )
        )
        print(conference.location)
        print(header_border)

        # Users
        print()
        print('Users')
        print('-----')

        start_datetime = datetime.combine(
            conference.start_date,
            datetime.max.time()
        ).astimezone()
        one_day_delta = timedelta(days=1)
        users = User.objects.\
            filter(date_joined__lt=(start_datetime - one_day_delta)).\
            exclude(pk__in=[1, 2, 3])
        print('Users at midnight before event began: %s' % users.count())

        day_number = 1
        date = conference.start_date
        while date <= conference.end_date:
            date_datetime = datetime.combine(
                date,
                datetime.max.time(),
            ).astimezone()
            users = User.objects.\
                filter(date_joined__lte=date_datetime).\
                exclude(pk__in=[1, 2, 3])
            print(
                'Users at midnight at end of day %s: %s'
                % (day_number, users.count())
            )
            day_number += 1
            date += one_day_delta

        one_week_later = conference.end_date + timedelta(days=7)
        one_week_later_datetime = datetime.combine(
            one_week_later,
            datetime.max.time(),
        ).astimezone()
        users = User.objects.\
            filter(date_joined__lt=one_week_later_datetime).\
            exclude(pk__in=[1, 2, 3])
        print('Users one week after event ended: %s' % users.count())

        nonadmin_profiles = Profile.objects.exclude(user__pk__in=[1, 2, 3])
        nonadmin_users = User.objects.exclude(pk__in=[1, 2, 3])
        nonempty_profiles = nonadmin_profiles.\
            filter(created__lt=F('modified') - timedelta(seconds=3))
        nonempty_profiles_percentage = round(
            (nonempty_profiles.count()/nonadmin_users.count()) * 100
        )
        print(
            'Users who filled out any of their profile: %s%% (%s users)'
            % (nonempty_profiles_percentage, nonempty_profiles.count())
        )

        users_with_email = nonadmin_users.exclude(email='')
        users_with_email_percentage = round(
            (users_with_email.count()/nonadmin_users.count() * 100)
        )
        print(
            'Users who gave their email address: %s%% (%s users)'
            % (users_with_email_percentage, users_with_email.count())
        )

        profiles_with_github = nonadmin_profiles.exclude(github='')
        profiles_with_github_percentage = round(
            (profiles_with_github.count()/nonadmin_users.count() * 100)
        )
        print(
            'Users who gave their Github username: %s%% (%s users)'
            % (profiles_with_github_percentage, profiles_with_github.count())
        )

        profiles_with_twitter = nonadmin_profiles.exclude(twitter='')
        profiles_with_twitter_percentage = round(
            (profiles_with_twitter.count()/nonadmin_users.count() * 100)
        )
        print(
            'Users who gave their Twitter handle: %s%% (%s users)'
            % (profiles_with_twitter_percentage, profiles_with_twitter.count())
        )

        # Conversations
        print()
        print('Conversations')
        print('-------------')

        all_conversations = Conversation.objects.all()
        conversations_not_initiated_by_admins = all_conversations.\
            exclude(initiator__pk__in=[1, 2, 3])

        print(
            'Conversations initiated: %s' %
            conversations_not_initiated_by_admins.count()
        )

        count = 0
        for c in conversations_not_initiated_by_admins:
            if c.messages.exclude(sender=c.initiator).exists():
                count += 1
        conversations_with_reply_percentage = round(
            (count/conversations_not_initiated_by_admins.count() * 100)
        )
        print(
            'Conversations with a reply to initial contact: %s%% '
            '(%s conversations)'
            % (conversations_with_reply_percentage, count)
        )

        initiators = []
        for c in conversations_not_initiated_by_admins:
            if c.initiator not in initiators:
                initiators.append(c.initiator)
        initiators_percentage = round(
            len(initiators)/nonadmin_users.count() * 100
        )
        print(
            'Users who initiated a conversation: %s%% (%s users)'
            % (initiators_percentage, len(initiators))
        )

        conversation_count = 0
        message_count = 0
        for c in all_conversations:
            if c.messages.exclude(sender=c.initiator).exists():
                conversation_count += 1
                message_count += c.messages.all().count()
        average_message_count = round(message_count/conversation_count, 1)
        print(
            'Messages per conversation where there was a reply to initial '
            'contact: %s' % average_message_count
        )

        conversations_initiated_by_admins = all_conversations.\
            filter(initiator__pk__in=[2, 3])
        print(
            'Conversations initiated by admins: %s'
            % conversations_initiated_by_admins.count()
        )

        count = 0
        for c in conversations_initiated_by_admins:
            if c.messages.exclude(sender=c.initiator).exists():
                count += 1
        if conversations_initiated_by_admins.exists():
            conversations_with_reply_percentage = round(
                (count/conversations_initiated_by_admins.count() * 100)
            )
        else:
            conversations_with_reply_percentage = 0

        print(
            'Conversations initiated by admins with a reply to initial '
            'contact: %s%% (%s conversations)'
            % (conversations_with_reply_percentage, count)
        )

        # Meetups
        print()
        print('Meetups')
        print('-------')

        meetups = Meetup.objects.all()
        print('Meetups: %s' % meetups.count())

        meetup_organisers = []
        for m in meetups:
            if m.organiser not in meetup_organisers:
                meetup_organisers.append(m.organiser)
        meetup_percentage = round(
            len(meetup_organisers)/nonadmin_users.count() * 100
        )
        print(
            'Users who created a meetup: %s%% (%s users)'
            % (meetup_percentage, len(meetup_organisers))
        )

        # Searches
        print()
        print('Searches')
        print('--------')

        print('Total number of profile searches: ')
        print('Run this command and paste the result in:')
        print(
            'grep "friendli.io/search/ --" ~/logs/requests.log | grep -v '
            '"User: 1 --" | grep -v "User: 2 --" | grep -v "User: 3 --" | '
            'grep -v "User: Anon --" | grep -F "csrfmiddlewaretoken" | wc -l'
        )

        print('Total number of username searches: ')
        print('Run this command and paste the result in:')
        print(
            'grep "friendli.io/username-search/ --" ~/logs/requests.log | '
            'grep -v "User: 1 --" | grep -v "User: 2 --" | grep -v "User: 3 '
            '--" | grep -v "User: Anon --" | grep -F "csrfmiddlewaretoken" | '
            'wc -l'
        )

        # Blocks, reports, stars.
        print()
        print('Blocks, reports, stars')
        print('----------------------')

        # Blocks
        blocks = Blocked.objects.all()
        print('Times one user blocked another user: %s' % blocks.count())

        # Reports
        reports = BehaviourReport.objects.all()
        print('Times one user reported another user: %s' % reports.count())

        # Stars
        starred = Starred.objects.all()
        print('Times one user starred another user: %s' % starred.count())

        starring_profiles = {p.starring_profile for p in starred}
        starring_percentage = round(
            len(starring_profiles)/nonadmin_users.count() * 100
        )
        print(
            'Users who starred another user: %s%% (%s users)'
            % (starring_percentage, len(starring_profiles))
        )

        # Languages
        print()
        print('Languages')
        print('---------')
        languages = Language.objects.all()
        languages_list = [l.language for l in languages]
        print('Options:')
        print(', '.join(languages_list))
        print('Frequency:')
        counter = Counter()
        for profile in nonadmin_profiles:
            counter.update(profile.languages.all())
        languages_dict = {}
        for language in languages:
            languages_dict[language.language] = counter[language]
        ordered_dict = OrderedDict(
            sorted(languages_dict.items(), key=lambda x: -1 * x[1])
        )
        strings_list = []
        for k, v in ordered_dict.items():
            strings_list.append(
                '%s (%s%%, %s users)'
                % (k, round((v/nonadmin_profiles.count()) * 100), v)
            )
        if strings_list:
            print(', '.join(strings_list))
        else:
            print('-')

        # Looking for
        print()
        print('Looking for')
        print('-----------')
        looking_fors = LookingFor.objects.all()
        looking_for_list = [lf.looking_for for lf in looking_fors]
        print('Options:')
        print(', '.join(looking_for_list))
        print('Frequency:')
        counter = Counter()
        for profile in nonadmin_profiles:
            counter.update(profile.looking_for.all())
        looking_for_dict = {}
        for looking_for in looking_fors:
            looking_for_dict[looking_for.looking_for] = counter[looking_for]
        ordered_dict = OrderedDict(
            sorted(looking_for_dict.items(), key=lambda x: -1 * x[1])
        )
        strings_list = []
        for k, v in ordered_dict.items():
            strings_list.append(
                '%s (%s%%, %s users)'
                % (k, round((v/nonadmin_profiles.count()) * 100), v)
            )
        if strings_list:
            print(', '.join(strings_list))
        else:
            print('-')

        # Personal interests
        print()
        print('Personal interests')
        print('------------------')
        personal_interests = PersonalInterest.objects.all()
        personal_interests_list = [
            pi.personal_interest for pi in personal_interests
        ]
        print('Options:')
        print(', '.join(personal_interests_list))
        print('Frequency:')
        counter = Counter()
        for profile in nonadmin_profiles:
            counter.update(profile.personal_interests.all())
        personal_interests_dict = {}
        for personal_interest in personal_interests:
            personal_interests_dict[personal_interest.personal_interest] = \
                counter[personal_interest]
        ordered_dict = OrderedDict(
            sorted(personal_interests_dict.items(), key=lambda x: -1 * x[1])
        )
        strings_list = []
        for k, v in ordered_dict.items():
            strings_list.append(
                '%s (%s%%, %s users)'
                % (k, round((v/nonadmin_profiles.count()) * 100), v)
            )
        if strings_list:
            print(', '.join(strings_list))
        else:
            print('-')

        print()
        print('Professional interests')
        print('----------------------')
        prof_interests = ProfessionalInterest.objects.all()
        prof_interests_list = [pi.prof_interest for pi in prof_interests]
        print('Options:')
        print(', '.join(prof_interests_list))
        print('Frequency:')
        counter = Counter()
        for profile in nonadmin_profiles:
            counter.update(profile.prof_interests.all())
        prof_interests_dict = {}
        for prof_interest in prof_interests:
            prof_interests_dict[prof_interest.prof_interest] = \
                counter[prof_interest]
        ordered_dict = OrderedDict(
            sorted(prof_interests_dict.items(), key=lambda x: -1 * x[1])
        )
        strings_list = []
        for k, v in ordered_dict.items():
            strings_list.append(
                '%s (%s%%, %s users)'
                % (k, round((v/nonadmin_profiles.count()) * 100), v)
            )
        if strings_list:
            print(', '.join(strings_list))
        else:
            print('-')

        print()
        print()
