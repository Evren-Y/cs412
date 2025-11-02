from django.db import models

# Create your models here.

class Voter(models.Model):
    '''Store one registered voter from Newton, MA.'''

    # identity
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)

    # address
    street_number = models.CharField(max_length=20, blank=True, null=True)
    street_name   = models.CharField(max_length=200, blank=True, null=True)
    apt_number    = models.CharField(max_length=50, blank=True, null=True)
    zip_code      = models.CharField(max_length=10, blank=True, null=True)

    # dates
    date_of_birth        = models.TextField(blank=True, null=True)
    date_of_registration = models.TextField(blank=True, null=True)

    # party
    party_affiliation = models.CharField(max_length=2, blank=True, null=True)

    # precinct
    precinct_number = models.CharField(max_length=10, blank=True, null=True)

    # participation flags
    v20state    = models.BooleanField(default=False)
    v21town     = models.BooleanField(default=False)
    v21primary  = models.BooleanField(default=False)
    v22general  = models.BooleanField(default=False)
    v23town     = models.BooleanField(default=False)

    # score
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        '''Return string representation of the Voter instance'''
        return f'{self.last_name}, {self.first_name} (P:{self.party_affiliation or "NA"}; Precinct:{self.precinct_number or "-"}) — Score {self.voter_score}'


def load_data():
    '''Function to load data records from CSV file into the Django database.'''

    filename = '\Users\evren\Downloads\newton_voters.csv'
    f = open(filename, 'r')  # open the file for reading

    # discard headers:
    f.readline()

    # helper to coerce Y/N-ish strings to bool (kept inline; no extra imports)
    def as_bool(s):
        if not s:
            return False
        s = s.strip().lower()
        return s in ('y', 'yes', 'true', 't', '1', 'x')

    created = 0

    # read the entire file, one line at a time (simple split like your marathon sample)
    for line in f:
        try:
            fields = line.strip().split(',')

            # index map
            #  0: Last Name
            #  1: First Name
            #  2: Residential Address - Street Number
            #  3: Residential Address - Street Name
            #  4: Residential Address - Apartment Number
            #  5: Residential Address - Zip Code
            #  6: Date of Birth
            #  7: Date of Registration
            #  8: Party Affiliation
            #  9: Precinct Number
            # 10: v20state
            # 11: v21town
            # 12: v21primary
            # 13: v22general
            # 14: v23town
            # 15: voter_score

            voter = Voter(
                last_name=fields[0].strip(),
                first_name=fields[1].strip(),

                street_number=fields[2].strip() or None,
                street_name=fields[3].strip() or None,
                apt_number=fields[4].strip() or None,
                zip_code=fields[5].strip() or None,

                # keep dates as text to avoid extra parsing imports
                date_of_birth=fields[6].strip() or None,
                date_of_registration=fields[7].strip() or None,

                # 2-char party
                party_affiliation=(fields[8].strip()[:2] if fields[8].strip() else None),

                precinct_number=fields[9].strip() or None,

                v20state=as_bool(fields[10] if len(fields) > 10 else ''),
                v21town=as_bool(fields[11] if len(fields) > 11 else ''),
                v21primary=as_bool(fields[12] if len(fields) > 12 else ''),
                v22general=as_bool(fields[13] if len(fields) > 13 else ''),
                v23town=as_bool(fields[14] if len(fields) > 14 else ''),

                voter_score=int(fields[15].strip()) if len(fields) > 15 and fields[15].strip().isdigit() else 0,
            )

            voter.save()
            created += 1

        except Exception:
            print("Something went wrong!")
            print(f"line={line}")

    print(f"Done. Created {created} Voters")
