-- ============================================================================
-- D1 Migration: program_registry — Canonical Program/Product WBS Registry
-- Target DB: portfolio-state (via qnfo-lifecycle Worker)
-- ADR: ADR-2026-007 (hierarchical WBS codes: portfolio > program > project > phase > task > subtask)
-- Created: 2026-08-04
-- ============================================================================

CREATE TABLE IF NOT EXISTS program_registry (
  wbs_code      TEXT PRIMARY KEY,
  level         TEXT NOT NULL,
  parent_wbs    TEXT,
  name          TEXT NOT NULL,
  slug          TEXT UNIQUE NOT NULL,
  short_name    TEXT,
  description   TEXT,
  github_repo   TEXT,
  zenodo_doi    TEXT,
  d1_slug       TEXT,
  kg_node_id    TEXT,
  current_version TEXT,
  phase         TEXT,
  status        TEXT DEFAULT 'active',
  wbs_order     INTEGER,
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (parent_wbs) REFERENCES program_registry(wbs_code)
);

CREATE INDEX IF NOT EXISTS idx_pr_level ON program_registry(level);
CREATE INDEX IF NOT EXISTS idx_pr_parent ON program_registry(parent_wbs);
CREATE INDEX IF NOT EXISTS idx_pr_slug ON program_registry(slug);
CREATE INDEX IF NOT EXISTS idx_pr_status ON program_registry(status);

-- Portfolio Root
INSERT OR REPLACE INTO program_registry (wbs_code, level, parent_wbs, name, slug, short_name, description, status, wbs_order)
VALUES ('QNFO', 'portfolio', NULL, 'QNFO Research Foundation', 'qnfo', 'QNFO',
        'QNFO Research Foundation — open-science research collective.', 'active', 0);

-- Programs
INSERT OR REPLACE INTO program_registry (wbs_code, level, parent_wbs, name, slug, short_name, description, zenodo_doi, status, wbs_order)
VALUES 
('QNFO.SR', 'program', 'QNFO', 'Silent Radix Cryptography', 'silent-radix', 'Silent Radix',
 'Positional notation cannot specify its own base; base-ambiguity as cryptographic primitive.', NULL, 'active', 1),
('QNFO.ADL', 'program', 'QNFO', 'Adelic Physics Program', 'adelic-physics', 'Adelic Physics',
 'Zitterbewegung as p-adic channel manifestation; adelic Shannon theory.', '10.5281/zenodo.21336099', 'active', 2),
('QNFO.PBO', 'program', 'QNFO', 'Pattern-Based Ontology (Autaxys)', 'pbo-autaxys', 'PBO/Autaxys',
 'Intrinsic self-ordering via Bruhat-Tits tree structures.', NULL, 'active', 3),
('QNFO.QD', 'program', 'QNFO', 'The Qubit Delusion', 'qubit-delusion', 'Qubit Delusion',
 '$35B quantum computing failure diagnosed as infinity-place projection error.', NULL, 'active', 4),
('QNFO.UF', 'program', 'QNFO', 'Ultrametric Foundations', 'ultrametric-foundations', 'Ultrametric Foundations',
 'p-adic valuations classify QEC codes at 83% accuracy.', '10.5281/zenodo.21046993', 'active', 5),
('QNFO.CON', 'program', 'QNFO', 'Cross-Pillar Consilience', 'cross-pillar-consilience', 'Consilience',
 'Five-pillar synthesis: ultrametric mathematics as correct state-space geometry.', '10.5281/zenodo.21547793', 'active', 6),
('QNFO.CMP', 'program', 'QNFO', 'Computing Machines', 'computing-machines', 'Computing Machines',
 'Computational architecture analysis and machine classification.', NULL, 'active', 7),
('QNFO.JPC', 'program', 'QNFO', 'JPCub Validation', 'jpcub-validation', 'JPCub Validation',
 'JPCUB benchmark validation and quantum computing performance assessment.', NULL, 'active', 8);

-- Projects
INSERT OR REPLACE INTO program_registry (wbs_code, level, parent_wbs, name, slug, short_name, description, github_repo, zenodo_doi, d1_slug, current_version, phase, status, wbs_order)
VALUES
('QNFO.ADL.001', 'project', 'QNFO.ADL', 'Adelic Shannon Theory', 'adelic-shannon-theory', 'Adelic Shannon',
 'Shannon-theoretic framework over adelic spaces.', 'QNFO/adelic-shannon-theory', '10.5281/zenodo.21336099', 'paper-adelic-shannon-v2', 'v2.0', NULL, 'active', 1),
('QNFO.ADL.002', 'project', 'QNFO.ADL', 'Adelic Entropic Numbers', 'adelic-entropic-numbers', 'Adelic Entropy',
 'Entropic number analysis in adelic function spaces.', 'QNFO/adelic-shannon-theory', NULL, NULL, 'v1.0', NULL, 'active', 2),
('QNFO.ADL.003', 'project', 'QNFO.ADL', 'Adelic Rate Distortion', 'adelic-rate-distortion', 'Adelic Rate-Distortion',
 'Rate-distortion theory over p-adic channels.', 'QNFO/adelic-shannon-theory', NULL, NULL, 'v1.0', NULL, 'active', 3),
('QNFO.CON.001', 'project', 'QNFO.CON', 'WBS.6 Consilient Synthesis', 'wbs-6-synthesis', 'Five Pillars Synthesis',
 'Five-pillar consilience paper demonstrating Adelic Core convergence.', 'QNFO/wbs-6-synthesis', '10.5281/zenodo.21547793', 'wbs-6-five-pillars-consilient-synthesis', 'v1.4', 'P8', 'complete', 1),
('QNFO.CMP.001', 'project', 'QNFO.CMP', 'Computing Machines', 'computing-machines', 'Computing Machines',
 'Computational architecture analysis.', 'QNFO/computing-machines', NULL, NULL, NULL, NULL, 'active', 1),
('QNFO.JPC.001', 'project', 'QNFO.JPC', 'JPCub Validation', 'jpcub-validation', 'JPCub Validation',
 'JPCUB benchmark validation.', 'QNFO/jpcub-validation', NULL, NULL, NULL, NULL, 'active', 1);

-- View: WBS tree with parent names
CREATE VIEW IF NOT EXISTS wbs_tree AS
SELECT p1.*, p2.name AS parent_name
FROM program_registry p1
LEFT JOIN program_registry p2 ON p1.parent_wbs = p2.wbs_code
ORDER BY p1.wbs_order, p1.wbs_code;
