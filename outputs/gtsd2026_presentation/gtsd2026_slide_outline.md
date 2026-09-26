# IEEE GTSD 2026 Presentation Outline
1. Title: A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification
2. Motivations: Agricultural Background & The Challenge
3. Motivations: Limitations of Existing AI Approaches (Whole-Image CNN vs Standalone YOLO)
4. Motivations: Research Objectives & Proposed Solution (Localize First, Classify Second)
5. Dataset Preparation: The BDPapayaLeaf Dataset & Rigorous Data Hygiene (~200 duplicates removed)
6. Dataset Preparation: Roboflow Annotation & ROI Extraction Strategy (Why NO boxes for Healthy)
7. Dataset Preparation: Addressing Class Imbalance & Data Augmentation (Class-weighted loss)
8. Framework: Overall System Architecture & Intelligent Routing Workflow
9. Framework: Stage 1 – YOLOv11m Detector Architecture (C3k2 Block & C2PSA Attention)
10. Framework: Stage 2 – EfficientNet-B2 Classifier Architecture (Compound Scaling & MBConv)
11. Framework: End-to-End Inference & Multi-Lesion Logic (~30-45ms latency)
12. Results: Stage 1 Detector Evaluation (YOLOv11m mAP@0.5 = 77.67%)
13. Results: Full Cascade vs. Baselines (+2.07% accuracy boost over whole-image baseline)
14. Results: Class-Wise Performance & Confusion Matrix (276/291 correct)
15. Results: Benchmarking Against Published Studies (Outperforming ResNet50, HASPNet, Darknet53)
16. Conclusion: Summary of Key Contributions
17. Conclusion: Future Work & Real-World Farm Deployment (Edge & Drone AI)
18. Conclusion: Thank You & Q&A
