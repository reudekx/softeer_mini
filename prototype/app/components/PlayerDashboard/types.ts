interface CommonStat {
  value: number;
  sites: string[];
}

interface CommonStats {
  [key: string]: CommonStat;
}

interface UniqueStat {
  stat: string;
  value: string;
  source: string;
}

interface SubjectiveDataBase {
  metric: string;
  average: number;
}

type SiteName = 'FotMob' | 'SofaScore' | 'FBref' | 'Understat' | 'Opta';

type SubjectiveData = SubjectiveDataBase & {
  [K in SiteName]?: number;
}

interface PlayerData {
  playerInfo: {
    name: string;
    team: string;
    position: string;
    photoUrl?: string;
  };
  commonStats: CommonStats;
  uniqueStats: UniqueStat[];
  subjectiveData: SubjectiveData[];
  siteFeatures: {
    siteName: string;
    features: string[];
  }[];
}