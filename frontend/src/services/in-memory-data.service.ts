export class InMemoryDataService {
    createDb() {
        let stages = [
            {
                id: 1,
                title: 'Your New Feature 1',
                endpoint: 'fn31dsk.stage34.org',
                repo: 'stage34',
                branch: 'issue-1-your-new-feature',
                status: 'paused',
                commits: 34,
                created_ts: 1471156891000
            }, {
                id: 2,
                title: 'Your New Feature 2',
                endpoint: 'dbh12dj.stage34.org',
                repo: 'stage34',
                branch: 'issue-2-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000
            }, {
                id: 3,
                title: 'Your New Feature 3',
                endpoint: 'j12d933.stage34.org',
                repo: 'stage34',
                branch: 'issue-3-your-new-feature',
                status: 'running',
                commits: 5,
                created_ts: 1471156691000
            }, {
                id: 4,
                title: 'Your New Feature 4',
                endpoint: 'dwnj18f.stage34.org',
                repo: 'stage34',
                branch: 'issue-4-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000
            }, {
                id: 5,
                title: 'Your New Feature 5',
                endpoint: 'dn12dn1.stage34.org',
                repo: 'stage34',
                branch: 'issue-5-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156821000
            }, {
                id: 6,
                title: 'Your New Feature 6',
                endpoint: 'njwed19.stage34.org',
                repo: 'stage34',
                branch: 'issue-6-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471151891000
            }, {
                id: 7,
                title: 'Your New Feature 7',
                endpoint: 'njw2an1.stage34.org',
                repo: 'stage34',
                branch: 'issue-7-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000
            }, {
                id: 8,
                title: 'Your New Feature 8',
                endpoint: 'njw120j.stage34.org',
                repo: 'stage34',
                branch: 'issue-8-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000
            }
        ];
    return { stages };
  }
}
